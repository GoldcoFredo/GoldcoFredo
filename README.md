# Product Management App - Version 0.3

## Overview

Welcome to the Product Management App, Version 0.3. This application is designed to provide a comprehensive environment for managing products, stores, and sales data. In this version, we have validated and included various functionalities to interact with the `Product` table in Snowflake. The core features include querying data, uploading flat files, executing tasks, and managing product data.

## Features

1. **Query Products**: Retrieve and display data from the `Product` table.
2. **Upload Flat Files to Stage**: Upload files to a Snowflake stage for further processing.
3. **Execute Bulk Load Task**: Execute the `BULK_LOAD_PRODUCTS` task to process data.
4. **Clear Product Stages**: Clear data from product stages.
5. **Truncate Product Table**: Clear all data from the `Product` table.
6. **Add Products**: Add new product entries to the `Product` table.

## Environment Setup

This environment is designed for managing three main tables:
- `Product`
- `Store`
- `Sales`

Each table will have corresponding functions and endpoints to interact with the data effectively.

## Prerequisites

Ensure you have the following software installed:
- Python 3.x
- Snowflake account
- Flask
- Visual Studio Code (optional, but recommended)
- Git

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/product-management-app.git
    cd product-management-app
    ```

2. Create and activate a virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

4. Set up environment variables for Snowflake configuration. Create a `.env` file in the project root with the following content:

    ```plaintext
    SNOWFLAKE_USER=your_user
    SNOWFLAKE_PASSWORD=your_password
    SNOWFLAKE_ACCOUNT=your_account
    SNOWFLAKE_WAREHOUSE=your_warehouse
    SNOWFLAKE_DATABASE=your_database
    SNOWFLAKE_SCHEMA=your_schema
    SNOWFLAKE_ROLE=your_role
    ```

## Running the Application

1. Start the Flask application:

    ```bash
    ./start.sh
    ```

2. Open your web browser and navigate to `http://localhost:8000` (or the URL provided by your deployment platform).

## Usage

### Query Products

To query products, click on the "Query Products" button in the sidebar. This will retrieve and display the data from the `Product` table.

### Upload to Stage

To upload a flat file to the Snowflake stage:
1. Click on the "Upload to Stage" button in the sidebar.
2. Select the file you want to upload.
3. Click the "Upload" button.

### Execute Task

To execute the `BULK_LOAD_PRODUCTS` task:
1. Click on the "Execute Task" button in the sidebar.
2. The task will be executed, and the data will be processed.

### Clear Product Stages

To clear the product stages:
1. Click on the "Clear Product Stages" button in the sidebar.
2. The stages will be cleared.

### Truncate Product Table

To truncate the `Product` table:
1. Click on the "Truncate Product Table" button in the sidebar.
2. The table will be truncated, removing all data.

### Add Products

To add a new product:
1. Click on the "Add Product" button in the sidebar.
2. Fill in the product details in the form.
3. Click the "Add Product" button to save the product.

## Future Plans

In the upcoming versions, we plan to:
- Add functionality to manage `Store` and `Sales` tables.
- Improve the user interface for better user experience.
- Add authentication and authorization features to secure the application.

## Contribution

Contributions are welcome! Please fork the repository and create a pull request with your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Thank you for using the Product Management App. If you have any questions or need further assistance, please feel free to contact us.
