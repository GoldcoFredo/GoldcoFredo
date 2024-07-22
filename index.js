document.addEventListener('DOMContentLoaded', () => {
    // Event listeners for form submissions and button clicks
    document.getElementById('add-product-form').addEventListener('submit', addProduct);
    document.getElementById('upload-form').addEventListener('submit', uploadFile);
    document.getElementById('edit-product-form').addEventListener('submit', editProduct);
    
    // Function to show a section
    window.showSection = function(sectionId) {
        document.querySelectorAll('.section').forEach(section => {
            section.classList.remove('visible');
        });
        document.getElementById(sectionId).classList.add('visible');
    };
    
    // Function to hide a section
    window.hideSection = function(sectionId) {
        document.getElementById(sectionId).classList.remove('visible');
    };

    // Function to retrieve products from the backend
    window.retrieveProducts = function() {
        fetch('https://gfbackend.onrender.com/products')
            .then(response => response.json())
            .then(data => {
                const tableBody = document.getElementById('product-table').getElementsByTagName('tbody')[0];
                tableBody.innerHTML = '';
                data.forEach(product => {
                    const row = tableBody.insertRow();
                    row.insertCell(0).textContent = product.ID_PRODUCT;
                    row.insertCell(1).textContent = product.PRODUCT_NAME;
                    row.insertCell(2).textContent = product.BRAND;
                    row.insertCell(3).textContent = product.HEIGHT;
                    row.insertCell(4).textContent = product.WIDTH;
                    row.insertCell(5).textContent = product.DEPTH;
                    row.insertCell(6).textContent = product.WEIGHT;
                    row.insertCell(7).textContent = product.PACKAGE_TYPE;
                    row.insertCell(8).textContent = product.PRICE;
                    const actionsCell = row.insertCell(9);
                    actionsCell.innerHTML = `
                        <button onclick="editProduct(${product.ID_PRODUCT})">Edit</button>
                        <button onclick="deleteProduct(${product.ID_PRODUCT})">Delete</button>
                    `;
                });
            })
            .catch(error => console.error('Error retrieving products:', error));
    };

    // Function to clear all products
    window.clearProducts = function() {
        fetch('https://gfbackend.onrender.com/clear-products', { method: 'POST' })
            .then(response => response.json())
            .then(data => alert(data.message))
            .catch(error => console.error('Error clearing products:', error));
    };

    // Function to clear the stage
    window.clearStage = function() {
        fetch('https://gfbackend.onrender.com/clear-stage', { method: 'POST' })
            .then(response => response.json())
            .then(data => alert(data.message))
            .catch(error => console.error('Error clearing stage:', error));
    };

    // Function to execute a task
    window.executeTask = function() {
        fetch('https://gfbackend.onrender.com/execute-task', { method: 'POST' })
            .then(response => response.json())
            .then(data => alert(data.message))
            .catch(error => console.error('Error executing task:', error));
    };

    // Function to add a product
    function addProduct(event) {
        event.preventDefault();
        const productName = document.getElementById('product-name').value;
        const brand = document.getElementById('brand').value;
        const height = parseFloat(document.getElementById('height').value);
        const width = parseFloat(document.getElementById('width').value);
        const depth = parseFloat(document.getElementById('depth').value);
        const weight = parseFloat(document.getElementById('weight').value);
        const packageType = document.getElementById('package-type').value;
        const price = parseFloat(document.getElementById('price').value);

        fetch('https://gfbackend.onrender.com/add-product', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                product_name: productName,
                brand: brand,
                height: height,
                width: width,
                depth: depth,
                weight: weight,
                package_type: packageType,
                price: price
            })
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            hideSection('add-product');
            retrieveProducts(); // Refresh product list
        })
        .catch(error => console.error('Error adding product:', error));
    }

    // Function to edit a product
    window.editProduct = function(id) {
        fetch(`https://gfbackend.onrender.com/products/${id}`)
            .then(response => response.json())
            .then(product => {
                document.getElementById('edit-id').value = product.ID_PRODUCT;
                document.getElementById('edit-product-name').value = product.PRODUCT_NAME;
                document.getElementById('edit-brand').value = product.BRAND;
                document.getElementById('edit-height').value = product.HEIGHT;
                document.getElementById('edit-width').value = product.WIDTH;
                document.getElementById('edit-depth').value = product.DEPTH;
                document.getElementById('edit-weight').value = product.WEIGHT;
                document.getElementById('edit-package-type').value = product.PACKAGE_TYPE;
                document.getElementById('edit-price').value = product.PRICE;
                showSection('edit-product');
            })
            .catch(error => console.error('Error fetching product for edit:', error));
    };

    // Function to handle editing the product
    function editProduct(event) {
        event.preventDefault();
        const id = document.getElementById('edit-id').value;
        const productName = document.getElementById('edit-product-name').value;
        const brand = document.getElementById('edit-brand').value;
        const height = parseFloat(document.getElementById('edit-height').value);
        const width = parseFloat(document.getElementById('edit-width').value);
        const depth = parseFloat(document.getElementById('edit-depth').value);
        const weight = parseFloat(document.getElementById('edit-weight').value);
        const packageType = document.getElementById('edit-package-type').value;
        const price = parseFloat(document.getElementById('edit-price').value);

        fetch(`https://gfbackend.onrender.com/edit-product/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                product_name: productName,
                brand: brand,
                height: height,
                width: width,
                depth: depth,
                weight: weight,
                package_type: packageType,
                price: price
            })
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            hideSection('edit-product');
            retrieveProducts(); // Refresh product list
        })
        .catch(error => console.error('Error editing product:', error));
    }

    // Function to delete a product
    window.deleteProduct = function(id) {
        fetch(`https://gfbackend.onrender.com/delete-product/${id}`, { method: 'DELETE' })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
                retrieveProducts(); // Refresh product list
            })
            .catch(error => console.error('Error deleting product:', error));
    };

    // Function to handle file upload
    function uploadFile(event) {
        event.preventDefault();
        const fileInput = document.getElementById('file-upload');
        const formData = new FormData();
        formData.append('file', fileInput.files[0]);

        fetch('https://gfbackend.onrender.com/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            hideSection('upload-to-stage');
        })
        .catch(error => console.error('Error uploading file:', error));
    }
});
