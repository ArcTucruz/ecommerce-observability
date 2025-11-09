// Admin Dashboard JavaScript
const API_BASE_URL = 'http://localhost:5001/api';

// Load dashboard on page load
document.addEventListener('DOMContentLoaded', () => {
    checkAdminAccess();
    loadStatistics();
    loadUsers();
    loadOrders();
    loadProducts();
});

// Check if user is admin
function checkAdminAccess() {
    const currentUser = JSON.parse(localStorage.getItem('currentUser'));
    if (!currentUser || !currentUser.is_admin) {
        alert('Access denied! Admin only.');
        window.location.href = '/';
    }
}

// Load Statistics
async function loadStatistics() {
    try {
        const response = await fetch(`${API_BASE_URL}/admin/stats`);
        const data = await response.json();
        
        document.getElementById('statUsers').textContent = data.total_users;
        document.getElementById('statProducts').textContent = data.total_products;
        document.getElementById('statOrders').textContent = data.total_orders;
        document.getElementById('statRevenue').textContent = `$${data.total_revenue.toFixed(2)}`;
    } catch (error) {
        console.error('Error loading statistics:', error);
    }
}

// Load Users
async function loadUsers() {
    try {
        const response = await fetch(`${API_BASE_URL}/admin/users`);
        const data = await response.json();
        
        const tbody = document.getElementById('usersTableBody');
        
        if (data.users.length === 0) {
            tbody.innerHTML = '<tr><td colspan="6" style="text-align: center; padding: 30px;">No users found</td></tr>';
            return;
        }
        
        tbody.innerHTML = data.users.map(user => `
            <tr>
                <td>${user.id}</td>
                <td>${user.username}</td>
                <td>${user.email}</td>
                <td>${user.full_name || 'N/A'}</td>
                <td>
                    ${user.is_admin 
                        ? '<span class="badge badge-admin">Admin</span>' 
                        : '<span class="badge badge-user">User</span>'}
                </td>
                <td>${new Date(user.created_at).toLocaleDateString()}</td>
            </tr>
        `).join('');
        
        window.usersData = data.users;
    } catch (error) {
        console.error('Error loading users:', error);
        document.getElementById('usersTableBody').innerHTML = 
            '<tr><td colspan="6" style="text-align: center; padding: 30px;">Error loading users</td></tr>';
    }
}

// Load Orders
async function loadOrders() {
    try {
        const response = await fetch(`${API_BASE_URL}/admin/orders`);
        const data = await response.json();
        
        const tbody = document.getElementById('ordersTableBody');
        
        if (data.orders.length === 0) {
            tbody.innerHTML = '<tr><td colspan="6" style="text-align: center; padding: 30px;">No orders found</td></tr>';
            return;
        }
        
        tbody.innerHTML = data.orders.map(order => `
            <tr>
                <td>${order.order_number}</td>
                <td>${order.user_id}</td>
                <td>$${order.total_amount.toFixed(2)}</td>
                <td>${order.status}</td>
                <td>${order.order_items ? order.order_items.length : 0} items</td>
                <td>${new Date(order.created_at).toLocaleDateString()}</td>
            </tr>
        `).join('');
        
        window.ordersData = data.orders;
    } catch (error) {
        console.error('Error loading orders:', error);
        document.getElementById('ordersTableBody').innerHTML = 
            '<tr><td colspan="6" style="text-align: center; padding: 30px;">Error loading orders</td></tr>';
    }
}

// Load Products
async function loadProducts() {
    try {
        const response = await fetch(`${API_BASE_URL}/products`);
        const data = await response.json();
        
        const tbody = document.getElementById('productsTableBody');
        
        if (data.products.length === 0) {
            tbody.innerHTML = '<tr><td colspan="6" style="text-align: center; padding: 30px;">No products found</td></tr>';
            return;
        }
        
        tbody.innerHTML = data.products.map(product => `
            <tr>
                <td>${product.id}</td>
                <td>${product.name}</td>
                <td>$${product.price.toFixed(2)}</td>
                <td>${product.stock_quantity}</td>
                <td>${product.category}</td>
                <td>
                    <button class="btn-action btn-edit" onclick="editProduct(${product.id})">Edit</button>
                    <button class="btn-action btn-delete" onclick="deleteProduct(${product.id})">Delete</button>
                </td>
            </tr>
        `).join('');
        
        window.productsData = data.products;
    } catch (error) {
        console.error('Error loading products:', error);
        document.getElementById('productsTableBody').innerHTML = 
            '<tr><td colspan="6" style="text-align: center; padding: 30px;">Error loading products</td></tr>';
    }
}

// Edit Product
async function editProduct(productId) {
    const newStock = prompt('Enter new stock quantity:');
    
    if (newStock === null) return;
    
    const stock = parseInt(newStock);
    if (isNaN(stock) || stock < 0) {
        alert('Invalid stock quantity!');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/admin/products/${productId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ stock_quantity: stock })
        });
        
        if (response.ok) {
            alert('Product updated successfully!');
            loadProducts();
            loadStatistics();
        } else {
            alert('Failed to update product');
        }
    } catch (error) {
        console.error('Error updating product:', error);
        alert('Error updating product');
    }
}

// Delete Product
async function deleteProduct(productId) {
    if (!confirm('Are you sure you want to delete this product?')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/admin/products/${productId}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            alert('Product deleted successfully!');
            loadProducts();
            loadStatistics();
        } else {
            alert('Failed to delete product');
        }
    } catch (error) {
        console.error('Error deleting product:', error);
        alert('Error deleting product');
    }
}

// Export Users to CSV
function exportUsers() {
    if (!window.usersData || window.usersData.length === 0) {
        alert('No users data to export');
        return;
    }
    
    const csvContent = convertToCSV(window.usersData, [
        'id', 'username', 'email', 'full_name', 'is_admin', 'created_at'
    ]);
    
    downloadCSV(csvContent, 'users.csv');
}

// Export Orders to CSV
function exportOrders() {
    if (!window.ordersData || window.ordersData.length === 0) {
        alert('No orders data to export');
        return;
    }
    
    const csvContent = convertToCSV(window.ordersData, [
        'order_number', 'user_id', 'total_amount', 'status', 'shipping_address', 'created_at'
    ]);
    
    downloadCSV(csvContent, 'orders.csv');
}

// Export Products to CSV
function exportProducts() {
    if (!window.productsData || window.productsData.length === 0) {
        alert('No products data to export');
        return;
    }
    
    const csvContent = convertToCSV(window.productsData, [
        'id', 'name', 'price', 'stock_quantity', 'category', 'created_at'
    ]);
    
    downloadCSV(csvContent, 'products.csv');
}

// Convert JSON to CSV
function convertToCSV(data, headers) {
    const csvRows = [];
    
    csvRows.push(headers.join(','));
    
    for (const row of data) {
        const values = headers.map(header => {
            const value = row[header];
            if (value === null || value === undefined) return '';
            const escaped = String(value).replace(/"/g, '""');
            return `"${escaped}"`;
        });
        csvRows.push(values.join(','));
    }
    
    return csvRows.join('\n');
}

// Download CSV file
function downloadCSV(csvContent, filename) {
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    
    if (link.download !== undefined) {
        const url = URL.createObjectURL(blob);
        link.setAttribute('href', url);
        link.setAttribute('download', filename);
        link.style.visibility = 'hidden';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }
}

// Show Add Product Modal
function showAddProductModal() {
    document.getElementById('addProductModal').style.display = 'flex';
}

// Close Add Product Modal
function closeAddProductModal() {
    document.getElementById('addProductModal').style.display = 'none';
    document.getElementById('addProductForm').reset();
}

// Add Product Form Submit Handler
window.addEventListener('load', function() {
    const form = document.getElementById('addProductForm');
    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const productData = {
                name: document.getElementById('productName').value,
                price: parseFloat(document.getElementById('productPrice').value),
                stock_quantity: parseInt(document.getElementById('productStock').value),
                category: document.getElementById('productCategory').value,
                description: document.getElementById('productDescription').value,
                image_url: document.getElementById('productImageUrl').value || '/static/images/default-product.jpg'
            };
            
            try {
                const response = await fetch(`${API_BASE_URL}/admin/products`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(productData)
                });
                
                if (response.ok) {
                    alert('✅ Product created successfully!');
                    closeAddProductModal();
                    loadProducts();
                    loadStatistics();
                } else {
                    const error = await response.json();
                    alert('❌ Failed to create product: ' + (error.error || 'Unknown error'));
                }
            } catch (error) {
                console.error('Error creating product:', error);
                alert('❌ Error creating product. Please try again.');
            }
        });
    }
});

// Logout Function
function logoutAdmin() {
    // Clear user data
    localStorage.removeItem('currentUser');
    localStorage.clear();
    
    // Show success message
    alert('✅ Logged out successfully!');
    
    // Redirect to home page
    window.location.href = '/';
}