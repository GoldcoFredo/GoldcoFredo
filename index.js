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
            .catch(error =>
