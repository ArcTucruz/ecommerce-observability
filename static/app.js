// API Configuration
const API_BASE_URL = 'http://localhost:5001/api';

// Global State
let currentUser = null;
let currentCart = null;
let allProducts = [];

// Initialize App
document.addEventListener('DOMContentLoaded', function() {
    // Load user from localStorage
    const savedUser = localStorage.getItem('currentUser');
    if (savedUser) {
        currentUser = JSON.parse(savedUser);
        updateUserInterface();

        // Show admin button if user is admin
        if (currentUser.is_admin) {
            document.getElementById('admin-btn').style.display = 'inline-block';
        }
    }
    
    // Setup form handlers
    setupAuthForms();
    setupCheckoutForm();
    
    // Load initial data
    loadProducts();
    
    // Show home page
    showPage('home');
});

// Page Navigation
function showPage(pageName) {
    // Hide all pages
    document.querySelectorAll('.page').forEach(page => {
        page.classList.remove('active');
    });
    
    // Show selected page
    const page = document.getElementById(pageName + '-page');
    if (page) {
        page.classList.add('active');
        
        // Load page-specific data
        if (pageName === 'products') {
            loadProducts();
        } else if (pageName === 'cart') {
            loadCart();
        } else if (pageName === 'orders') {
            if (currentUser) {
                loadOrders();
            } else {
                showToast('Please login first', 'error');
                showPage('login');
            }
        } else if (pageName === 'checkout') {
            if (currentUser) {
                loadCheckout();
            } else {
                showToast('Please login first', 'error');
                showPage('login');
            }
        }
    }
}

// Authentication
function setupAuthForms() {
    // Login form
    document.getElementById('login-form').addEventListener('submit', async function(e) {
        e.preventDefault();
        const username = document.getElementById('login-username').value;
        const password = document.getElementById('login-password').value;
        
        try {
            const response = await fetch(`${API_BASE_URL}/users/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                currentUser = data.user;
                localStorage.setItem('currentUser', JSON.stringify(currentUser));
                updateUserInterface();

                // Show admin button if user is admin
                if (currentUser.is_admin) {
                    document.getElementById('admin-btn').style.display = 'inline-block';
                } else {
                    document.getElementById('admin-btn').style.display = 'none';
                }
                
                showToast('Login successful!', 'success');
                showPage('products');
            } else {
                document.getElementById('login-error').textContent = data.error;
            }
        } catch (error) {
            document.getElementById('login-error').textContent = 'Connection error. Please try again.';
        }
    });
    
    // Register form
    document.getElementById('register-form').addEventListener('submit', async function(e) {
        e.preventDefault();
        const fullName = document.getElementById('register-fullname').value;
        const username = document.getElementById('register-username').value;
        const email = document.getElementById('register-email').value;
        const password = document.getElementById('register-password').value;
        
        try {
            const response = await fetch(`${API_BASE_URL}/users/register`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    username, 
                    email, 
                    password, 
                    full_name: fullName 
                })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                showToast('Registration successful! Please login.', 'success');
                switchAuthTab('login');
                document.getElementById('login-username').value = username;
            } else {
                document.getElementById('register-error').textContent = data.error;
            }
        } catch (error) {
            document.getElementById('register-error').textContent = 'Connection error. Please try again.';
        }
    });
}

function switchAuthTab(tab) {
    // Update tabs
    document.querySelectorAll('.auth-tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.auth-form').forEach(f => f.classList.remove('active'));
    
    if (tab === 'login') {
        document.querySelector('.auth-tab:first-child').classList.add('active');
        document.getElementById('login-form').classList.add('active');
    } else {
        document.querySelector('.auth-tab:last-child').classList.add('active');
        document.getElementById('register-form').classList.add('active');
    }
}

function updateUserInterface() {
    const userInfo = document.getElementById('user-info');
    const authBtn = document.getElementById('auth-btn');
    
    if (currentUser) {
        userInfo.textContent = `Hi, ${currentUser.username}!`;
        authBtn.textContent = 'Logout';
        authBtn.onclick = logout;
        loadCart();
    } else {
        userInfo.textContent = '';
        authBtn.textContent = 'Login';
        authBtn.onclick = () => showPage('login');
        updateCartCount(0);
    }
}

function logout() {
    currentUser = null;
    currentCart = null;
    localStorage.removeItem('currentUser');
    updateUserInterface();
    document.getElementById('admin-btn').style.display = 'none';
    showToast('Logged out successfully', 'success');
    showPage('home');
}

// Products
async function loadProducts() {
    try {
        const response = await fetch(`${API_BASE_URL}/products`);
        const data = await response.json();
        
        allProducts = data.products;
        displayProducts(allProducts);
    } catch (error) {
        showToast('Error loading products', 'error');
    }
}

function displayProducts(products) {
    const grid = document.getElementById('products-grid');
    
    if (products.length === 0) {
        grid.innerHTML = '<div class="loading">No products found</div>';
        return;
    }
    
    grid.innerHTML = products.map(product => {
    const imageHtml = product.image_url 
        ? `<img src="${product.image_url}" alt="${product.name}" style="width: 100%; height: 100%; object-fit: cover;">` 
        : '📦';
    
    return `
        <div class="product-card">
            <div class="product-image">${imageHtml}</div>
            <div class="product-info">
                <div class="product-name">${product.name}</div>
                <div class="product-description">${product.description || 'No description'}</div>
                <div class="product-price">$${product.price.toFixed(2)}</div>
                <div class="product-stock">Stock: ${product.stock_quantity}</div>
                <div class="product-actions">
                    <input type="number" id="qty-${product.id}" value="1" min="1" max="${product.stock_quantity}">
                    <button onclick="addToCart(${product.id})" class="btn-primary" 
                        ${product.stock_quantity === 0 ? 'disabled' : ''}>
                        ${product.stock_quantity === 0 ? 'Out of Stock' : 'Add to Cart'}
                    </button>
                </div>
            </div>
        </div>
    `;
}).join('');
}

// Cart
async function addToCart(productId) {
    if (!currentUser) {
        showToast('Please login first', 'error');
        showPage('login');
        return;
    }
    
    const quantity = parseInt(document.getElementById(`qty-${productId}`).value);
    
    try {
        const response = await fetch(`${API_BASE_URL}/cart/${currentUser.id}/add`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ product_id: productId, quantity })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            currentCart = data.cart;
            updateCartCount(data.cart.item_count);
            showToast('Added to cart!', 'success');
        } else {
            showToast(data.error, 'error');
        }
    } catch (error) {
        showToast('Error adding to cart', 'error');
    }
}

async function loadCart() {
    if (!currentUser) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/cart/${currentUser.id}`);
        const data = await response.json();
        
        if (response.ok) {
            currentCart = data;
            displayCart(data);
            updateCartCount(data.item_count);
        }
    } catch (error) {
        showToast('Error loading cart', 'error');
    }
}

function displayCart(cart) {
    const cartItems = document.getElementById('cart-items');
    const cartSummary = document.getElementById('cart-summary');
    
    if (!cart.items || cart.items.length === 0) {
        cartItems.innerHTML = '<p class="empty-cart">Your cart is empty</p>';
        cartSummary.style.display = 'none';
        return;
    }
    
    cartItems.innerHTML = cart.items.map(item => `
        <div class="cart-item">
            <div class="cart-item-image">📦</div>
            <div class="cart-item-info">
                <div class="cart-item-name">${item.product.name}</div>
                <div class="cart-item-price">$${item.product.price.toFixed(2)} x ${item.quantity}</div>
            </div>
            <div class="cart-item-price">$${item.subtotal.toFixed(2)}</div>
            <button onclick="removeFromCart(${item.product.id})" class="btn-primary">Remove</button>
        </div>
    `).join('');
    
    cartSummary.style.display = 'block';
    document.getElementById('summary-items').textContent = cart.item_count;
    document.getElementById('summary-total').textContent = `$${cart.total.toFixed(2)}`;
}

async function removeFromCart(productId) {
    try {
        const response = await fetch(`${API_BASE_URL}/cart/${currentUser.id}/remove/${productId}`, {
            method: 'DELETE'
        });
        
        const data = await response.json();
        
        if (response.ok) {
            currentCart = data.cart;
            displayCart(data.cart);
            updateCartCount(data.cart.item_count);
            showToast('Item removed', 'success');
        } else {
            showToast(data.error, 'error');
        }
    } catch (error) {
        showToast('Error removing item', 'error');
    }
}

function updateCartCount(count) {
    document.getElementById('cart-count').textContent = count;
}

// Checkout
function loadCheckout() {
    if (!currentCart || !currentCart.items || currentCart.items.length === 0) {
        showToast('Your cart is empty', 'error');
        showPage('cart');
        return;
    }
}

function setupCheckoutForm() {
    document.getElementById('checkout-form').addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const shippingAddress = document.getElementById('shipping-address').value;
        const paymentMethod = document.getElementById('payment-method').value;
        
        try {
            const response = await fetch(`${API_BASE_URL}/orders`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    user_id: currentUser.id,
                    shipping_address: shippingAddress,
                    payment_method: paymentMethod
                })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                showToast('Order placed successfully!', 'success');
                currentCart = null;
                updateCartCount(0);
                showPage('orders');
                loadOrders();
            } else {
                showToast(data.error, 'error');
            }
        } catch (error) {
            showToast('Error placing order', 'error');
        }
    });
}

// Orders
async function loadOrders() {
    if (!currentUser) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/orders/user/${currentUser.id}`);
        const data = await response.json();
        
        if (response.ok) {
            displayOrders(data.orders);
        }
    } catch (error) {
        showToast('Error loading orders', 'error');
    }
}

function displayOrders(orders) {
    const ordersList = document.getElementById('orders-list');
    
    if (!orders || orders.length === 0) {
        ordersList.innerHTML = '<p class="empty-orders">No orders yet</p>';
        return;
    }
    
    ordersList.innerHTML = orders.map(order => `
        <div class="order-card">
            <div class="order-header">
                <div>
                    <div class="order-number">Order #${order.order_number}</div>
                    <div style="color: #7f8c8d; font-size: 0.9rem;">
                        ${new Date(order.created_at).toLocaleDateString()}
                    </div>
                </div>
                <span class="order-status ${order.status}">${order.status.toUpperCase()}</span>
            </div>
            <div style="margin: 1rem 0;">
                ${order.items.map(item => `
                    <div style="display: flex; justify-content: space-between; padding: 0.5rem 0;">
                        <span>${item.product_name} x${item.quantity}</span>
                        <span>$${item.subtotal.toFixed(2)}</span>
                    </div>
                `).join('')}
            </div>
            <div style="display: flex; justify-content: space-between; padding-top: 1rem; border-top: 2px solid #ecf0f1; font-weight: bold; font-size: 1.2rem; color: #27ae60;">
                <span>Total</span>
                <span>$${order.total_amount.toFixed(2)}</span>
            </div>
            <div style="margin-top: 1rem; color: #7f8c8d; font-size: 0.9rem;">
                <strong>Shipping:</strong> ${order.shipping_address}
            </div>
        </div>
    `).join('');
}

// Toast Notification
function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = `toast ${type} show`;
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);

}

    // Admin Panel
function showAdminPanel() {
    window.location.href = '/admin.html';

}

