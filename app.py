from flask import Flask, request, jsonify
import snowflake.connector
import os

app = Flask(__name__)

# Load Snowflake connection parameters from environment variables
conn = snowflake.connector.connect(
    user=os.getenv('SNOWFLAKE_USER'),
    password=os.getenv('SNOWFLAKE_PASSWORD'),
    account=os.getenv('SNOWFLAKE_ACCOUNT'),
    warehouse=os.getenv('SNOWFLAKE_WAREHOUSE'),
    database=os.getenv('SNOWFLAKE_DATABASE'),
    schema=os.getenv('SNOWFLAKE_SCHEMA'),
    role=os.getenv('SNOWFLAKE_ROLE')
)

# Create a cursor object
cur = conn.cursor()

@app.route('/upload_to_stage', methods=['POST'])
def upload_to_stage():
    file_path = request.json.get('file_path')
    stage_name = "STAGE_PRODUCTS"
    try:
        put_command = f"PUT 'file:///{file_path.replace('\\', '\\\\')}' @{stage_name}"
        cur.execute(put_command)
        return jsonify({"message": f"File {file_path} uploaded to stage {stage_name}"}), 200
    except snowflake.connector.errors.ProgrammingError as e:
        return jsonify({"error": f"Error uploading file: {e}"}), 500

@app.route('/execute_task', methods=['POST'])
def execute_task():
    task_name = "BULK_LOAD_PRODUCTS"
    try:
        execute_task_command = f"EXECUTE TASK {task_name};"
        cur.execute(execute_task_command)
        return jsonify({"message": f"Task {task_name} executed"}), 200
    except snowflake.connector.errors.ProgrammingError as e:
        return jsonify({"error": f"Error executing task: {e}"}), 500

@app.route('/query_products', methods=['GET'])
def query_products():
    try:
        cur.execute("SELECT * FROM Product;")
        results = cur.fetchall()
        return jsonify(results), 200
    except snowflake.connector.errors.ProgrammingError as e:
        return jsonify({"error": f"Error querying products: {e}"}), 500

@app.route('/add_product', methods=['POST'])
def add_product():
    data = request.json
    try:
        insert_command = """
        INSERT INTO Product (ID_PRODUCT, PRODUCT_NAME, BRAND, HEIGHT, WIDTH, DEPTH, WEIGHT, PACKAGE_TYPE, PRICE)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        cur.execute(insert_command, (
            data['id_product'], data['product_name'], data['brand'], data['height'],
            data['width'], data['depth'], data['weight'], data['package_type'], data['price']
        ))
        return jsonify({"message": f"Product {data['product_name']} added to the Product table"}), 200
    except snowflake.connector.errors.ProgrammingError as e:
        return jsonify({"error": f"Error adding product: {e}"}), 500

@app.route('/clear_product_stages', methods=['POST'])
def clear_product_stages():
    try:
        remove_command_1 = "REMOVE @STAGE_HISTORIC_PRODUCTS;"
        remove_command_2 = "REMOVE @STAGE_PRODUCTS;"
        cur.execute(remove_command_1)
        cur.execute(remove_command_2)
        return jsonify({"message": "Removed files from stages"}), 200
    except snowflake.connector.errors.ProgrammingError as e:
        return jsonify({"error": f"Error clearing product stages: {e}"}), 500

@app.route('/truncate_product_table', methods=['POST'])
def truncate_product_table():
    try:
        truncate_command = "TRUNCATE TABLE Product;"
        cur.execute(truncate_command)
        return jsonify({"message": "Product table truncated"}), 200
    except snowflake.connector.errors.ProgrammingError as e:
        return jsonify({"error": f"Error truncating product table: {e}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 8080)))
