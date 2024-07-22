import snowflake.connector
from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import os

# Initialize Flask application
app = Flask(__name__)
CORS(app)  # Enable CORS for all origins

# Logging configuration
logging.basicConfig(level=logging.DEBUG)

# Function to get Snowflake connection
def get_snowflake_connection():
    return snowflake.connector.connect(
        user=os.getenv('SNOWFLAKE_USER'),
        password=os.getenv('SNOWFLAKE_PASSWORD'),
        account=os.getenv('SNOWFLAKE_ACCOUNT'),
        warehouse=os.getenv('SNOWFLAKE_WAREHOUSE'),
        database=os.getenv('SNOWFLAKE_DATABASE'),
        schema=os.getenv('SNOWFLAKE_SCHEMA'),
        role=os.getenv('SNOWFLAKE_ROLE')
    )

# Route to upload file to Snowflake stage
@app.route('/uploadToStage', methods=['POST'])
def upload_to_stage():
    stage_name = "STAGE_PRODUCTS"
    try:
        conn = get_snowflake_connection()
        cur = conn.cursor()

        # Get the file from the request
        if 'file' not in request.files:
            return jsonify({'message': 'No file part'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'message': 'No selected file'}), 400

        # Save the file to a temporary location
        file_path = os.path.join('/tmp', file.filename)
        file.save(file_path)

        put_command = f"PUT 'file://{file_path.replace('/', '//')}' @{stage_name}"
        cur.execute(put_command)
        conn.commit()
        logging.info(f"File {file_path} uploaded to stage {stage_name}")
        return jsonify({'message': f"File {file.filename} uploaded to stage {stage_name}"}), 200
    except Exception as e:
        logging.error(f"Error uploading file: {e}")
        return jsonify({'message': f"Error uploading file: {e}"}), 500
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
        # Clean up the temporary file
        if os.path.exists(file_path):
            os.remove(file_path)

# Route to execute Snowflake task
@app.route('/executeTask', methods=['POST'])
def execute_task():
    task_name = "BULK_LOAD_PRODUCTS"
    try:
        conn = get_snowflake_connection()
        cur = conn.cursor()

        execute_command = f"EXECUTE TASK {task_name}"
        cur.execute(execute_command)
        conn.commit()
        logging.info(f"Task {task_name} executed")
        return jsonify({'message': f"Task {task_name} executed"}), 200
    except Exception as e:
        logging.error(f"Error executing task: {e}")
        return jsonify({'message': f"Error executing task: {e}"}), 500
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

# Route to query products from Snowflake
@app.route('/queryProducts', methods=['GET'])
def query_products():
    try:
        conn = get_snowflake_connection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM Product;")
        results = cur.fetchall()
        product_data = [{'id_product': row[0], 'product_name': row[1], 'brand': row[2], 'height': row[3],
                         'width': row[4], 'depth': row[5], 'weight': row[6], 'package_type': row[7],
                         'price': row[8]} for row in results]
        return jsonify(product_data), 200
    except Exception as e:
        logging.error(f"Error querying products: {e}")
        return jsonify({'message': f"Error querying products: {e}"}), 500
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

# Route to add a product to Snowflake
@app.route('/addProduct', methods=['POST'])
def add_product():
    try:
        conn = get_snowflake_connection()
        cur = conn.cursor()

        data = request.json
        id_product = data.get('id_product')
        product_name = data.get('product_name')
        brand = data.get('brand')
        height = data.get('height')
        width = data.get('width')
        depth = data.get('depth')
        weight = data.get('weight')
        package_type = data.get('package_type')
        price = data.get('price')

        insert_command = f"""
        INSERT INTO Product (ID_PRODUCT, PRODUCT_NAME, BRAND, HEIGHT, WIDTH, DEPTH, WEIGHT, PACKAGE_TYPE, PRICE)
        VALUES ('{id_product}', '{product_name}', '{brand}', {height}, {width}, {depth}, {weight}, '{package_type}', {price});
        """
        cur.execute(insert_command)
        conn.commit()
        logging.info(f"Product {product_name} added to the Product table")
        return jsonify({'message': f"Product {product_name} added to the Product table"}), 200
    except Exception as e:
        logging.error(f"Error adding product: {e}")
        return jsonify({'message': f"Error adding product: {e}"}), 500
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

# Route to clear Snowflake product stages
@app.route('/clearProductStages', methods=['POST'])
def clear_stages():
    try:
        conn = get_snowflake_connection()
        cur = conn.cursor()

        cur.execute("REMOVE @stage_historic_products")
        cur.execute("REMOVE @stage_products")
        conn.commit()
        logging.info("All product stages cleared")
        return jsonify({'message': "All product stages cleared"}), 200
    except Exception as e:
        logging.error(f"Error clearing stages: {e}")
        return jsonify({'message': f"Error clearing stages: {e}"}), 500
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

# Route to truncate Snowflake product table
@app.route('/truncateProductTable', methods=['POST'])
def clear_product_table():
    try:
        conn = get_snowflake_connection()
        cur = conn.cursor()

        cur.execute("TRUNCATE TABLE Product")
        conn.commit()
        logging.info("Product table cleared")
        return jsonify({'message': "Product table cleared"}), 200
    except Exception as e:
        logging.error(f"Error clearing product table: {e}")
        return jsonify({'message': f"Error clearing product table: {e}"}), 500
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

# Close the cursor and connection
@app.teardown_appcontext
def close_connection(exception):
    if 'conn' in globals():
        conn.close()
    if 'cur' in globals():
        cur.close()

if __name__ == "__main__":
    app.run(debug=True)
