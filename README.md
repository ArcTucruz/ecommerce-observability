# E-Commerce Application with Observability

A full-stack e-commerce web application built with Flask backend and vanilla JavaScript frontend, featuring comprehensive observability implementation (Logs, Metrics, and Traces) and an admin dashboard for management.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Observability Implementation](#observability-implementation)
- [Architecture & Flow](#architecture--flow)
- [Project Structure](#project-structure)
- [Installation & Setup](#installation--setup)
- [API Endpoints](#api-endpoints)
- [Usage](#usage)

---

## 🎯 Overview

This project demonstrates a production-ready e-commerce platform with built-in observability features. It showcases the three pillars of observability: **Logs**, **Metrics**, and **Traces**, making it ideal for monitoring application health, user behavior, and system performance.

**Key Highlights:**
- Complete e-commerce functionality (products, cart, orders)
- Admin dashboard for management
- Real-time metrics collection
- Detailed logging with emojis for easy scanning
- Distributed tracing capability
- RESTful API design
- Responsive frontend

---

## ✨ Features

### User Features
- **User Authentication**
  - User registration with validation
  - Secure login/logout
  - Password hashing with Werkzeug
  
- **Product Browsing**
  - View product catalog with images
  - Product details (price, description, stock)
  - Category-based organization
  
- **Shopping Cart**
  - Add/remove products
  - Update quantities
  - Real-time cart total calculation
  - Persistent cart per user
  
- **Order Management**
  - Checkout process
  - Order creation with unique order numbers
  - Order history viewing
  - Shipping address input
  - Payment method selection

### Admin Features
- **Admin Dashboard**
  - Modern sidebar navigation
  - Statistics overview (users, products, orders, revenue)
  - Real-time data visualization
  
- **User Management**
  - View all registered users
  - User role identification (Admin/User badges)
  - Export users to CSV
  
- **Product Management**
  - View all products in table format
  - Add new products with modal form
  - Edit product stock quantities
  - Delete products
  - Export products to CSV
  
- **Order Management**
  - View all orders
  - Order details (items, amounts, status)
  - Export orders to CSV

### Observability Features

#### 1. **Logs** 📝
- **Comprehensive Activity Logging**
  - User registration and login attempts
  - Product operations (add, view, update, delete)
  - Cart operations (add, remove items)
  - Order creation and management
  - Admin actions tracking
  - HTTP request logging with status codes
  
- **Log Features**
  - Emoji indicators for easy scanning (🔐 ✅ ❌ 🛒 📊 💥)
  - Timestamp for each event
  - Log levels (INFO, WARNING, ERROR)
  - Detailed error messages with stack traces
  - File-based logging (`app.log`)

#### 2. **Metrics** 📊
- **Business Metrics**
  - `ecommerce_user_registrations_total` - Total user signups
  - `ecommerce_user_logins_total{status}` - Login attempts (success/failure)
  - `ecommerce_cart_additions_total` - Items added to cart
  - `ecommerce_orders_total` - Orders created
  - `ecommerce_order_value` - Revenue tracking
  
- **System Metrics** (via Prometheus Flask Exporter)
  - `flask_http_request_total` - HTTP request counts by method/status
  - `flask_http_request_duration_seconds` - Request latency
  - `process_*` - Python process metrics (CPU, memory)
  
- **Metrics Endpoint**
  - `/metrics` - Prometheus-compatible metrics endpoint
  - Scrape interval: 15 seconds (configurable)

#### 3. **Traces** 🔍
- **OpenTelemetry Integration**
  - Request tracing across the application
  - Database query tracing (SQLAlchemy instrumentation)
  - Service-to-service call tracking
  - Trace context propagation
  - Span attributes for detailed analysis

---

## 🛠️ Technology Stack

### Backend
- **Flask** - Web framework
- **Flask-SQLAlchemy** - ORM for database operations
- **Flask-CORS** - Cross-Origin Resource Sharing support
- **Werkzeug** - Password hashing and security utilities
- **SQLite** - Database (easily replaceable with PostgreSQL/MySQL)

### Observability
- **prometheus-flask-exporter** - Metrics collection and exposition
- **opentelemetry-api** - OpenTelemetry API for tracing
- **opentelemetry-sdk** - OpenTelemetry SDK implementation
- **opentelemetry-instrumentation-flask** - Flask auto-instrumentation
- **opentelemetry-instrumentation-sqlalchemy** - SQLAlchemy auto-instrumentation

### Frontend
- **Vanilla JavaScript** - No framework dependencies
- **HTML5 & CSS3** - Responsive design
- **Fetch API** - RESTful API communication

### Development Tools
- **Python logging** - Built-in logging module with custom configuration
- **dotenv** - Environment variable management

---

## 📊 Observability Implementation

### How Observability is Implemented

#### Logs Implementation
**Location:** Throughout the application
**Files involved:**
- `app/__init__.py` - Logger configuration
- `app/services/*.py` - Service-level logging
- `app/routes/*.py` - Request/response logging

**Key Features:**
```python
# Logger setup with file and console handlers
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

# Usage examples:
logger.info(f"✅ Login successful: '{username}' (ID: {user.id}) → HTTP 200")
logger.warning(f"❌ Login failed: Wrong password for user '{username}' → HTTP 401")
logger.error(f"💥 Server error during login: {str(e)} → HTTP 500")
```

#### Metrics Implementation
**Location:** `app/__init__.py` and service layers
**Endpoint:** `http://localhost:5000/metrics`

**Setup:**
```python
from prometheus_flask_exporter import PrometheusMetrics

# Initialize Prometheus metrics
metrics = PrometheusMetrics(app)

# Custom business metrics
user_registrations = Counter('ecommerce_user_registrations_total', 
                            'Total number of user registrations')
user_logins = Counter('ecommerce_user_logins_total', 
                     'Total number of login attempts', 
                     ['status'])
cart_additions = Counter('ecommerce_cart_additions_total', 
                        'Total number of products added to cart')
orders_total = Counter('ecommerce_orders_total', 
                      'Total number of orders created')
```

**Usage in services:**
```python
# Increment metrics when events occur
user_registrations.inc()
user_logins.labels(status='success').inc()
cart_additions.inc()
orders_total.inc()
```

#### Traces Implementation
**Location:** `app/__init__.py`
**Auto-instrumentation enabled for:**
- HTTP requests (Flask)
- Database queries (SQLAlchemy)

**Setup:**
```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor

# Initialize tracing
trace.set_tracer_provider(TracerProvider())
FlaskInstrumentor().instrument_app(app)
SQLAlchemyInstrumentor().instrument(engine=db.engine)
```

**What gets traced:**
- Every HTTP request with timing
- Database query execution
- Service method calls
- Error occurrences

---

## 🏗️ Architecture & Flow

### Application Flow
```
┌─────────────────────────────────────────────────────────────┐
│                        USER/ADMIN                            │
└──────────────┬──────────────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND (Browser)                        │
│  - HTML/CSS/JavaScript                                       │
│  - Fetch API for HTTP requests                               │
│  - LocalStorage for session management                       │
└──────────────┬──────────────────────────────────────────────┘
               │ HTTP/REST API
               ▼
┌─────────────────────────────────────────────────────────────┐
│                   FLASK BACKEND (Python)                     │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Routes Layer (app/routes/*.py)                       │  │
│  │  - users.py    - User authentication                  │  │
│  │  - products.py - Product catalog                      │  │
│  │  - cart.py     - Shopping cart operations             │  │
│  │  - orders.py   - Order management                     │  │
│  │  - admin.py    - Admin dashboard APIs                 │  │
│  └──────────────┬───────────────────────────────────────┘  │
│                 │                                            │
│  ┌──────────────▼───────────────────────────────────────┐  │
│  │  Services Layer (app/services/*.py)                   │  │
│  │  - user_service.py    - Business logic for users      │  │
│  │  - product_service.py - Business logic for products   │  │
│  │  - cart_service.py    - Business logic for cart       │  │
│  │  - order_service.py   - Business logic for orders     │  │
│  │  - admin_service.py   - Business logic for admin      │  │
│  └──────────────┬───────────────────────────────────────┘  │
│                 │                                            │
│  ┌──────────────▼───────────────────────────────────────┐  │
│  │  Models Layer (app/models/*.py)                       │  │
│  │  - user.py    - User entity                           │  │
│  │  - product.py - Product entity                        │  │
│  │  - cart.py    - Cart entity                           │  │
│  │  - order.py   - Order & OrderItem entities            │  │
│  └──────────────┬───────────────────────────────────────┘  │
│                 │                                            │
└─────────────────┼────────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│                   DATABASE (SQLite)                          │
│  - users table                                               │
│  - products table                                            │
│  - carts table                                               │
│  - orders table                                              │
│  - order_items table                                         │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│               OBSERVABILITY LAYER (Cross-cutting)            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │    LOGS      │  │   METRICS    │  │    TRACES    │     │
│  │  app.log     │  │  /metrics    │  │ OpenTelemetry│     │
│  │  (file)      │  │  endpoint    │  │  (spans)     │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

### Request Flow Example

**User Login Flow:**

1. **Frontend:** User enters username/password → JavaScript sends POST to `/api/users/login`
2. **Route:** `users.py` receives request → Validates input → Calls `UserService.authenticate_user()`
3. **Service:** `user_service.py` queries database → Checks password hash → Records metric → Logs event
4. **Response:** Returns user data → Frontend stores in localStorage → Updates UI
5. **Observability:**
   - **Log:** `✅ Login successful: 'admin' (ID: 1) → HTTP 200`
   - **Metric:** `ecommerce_user_logins_total{status="success"}` incremented
   - **Trace:** Span created for request with timing

**Add to Cart Flow:**

1. **Frontend:** User clicks "Add to Cart" → POST to `/api/cart/add`
2. **Route:** `cart.py` receives request → Validates product/quantity → Calls `CartService.add_to_cart()`
3. **Service:** `cart_service.py` checks stock → Updates cart in database → Logs action
4. **Response:** Returns updated cart → Frontend updates cart count
5. **Observability:**
   - **Log:** `🛒 Added to cart: 'Gaming Laptop' x1 (User: 1, Price: $1499.99) → HTTP 200`
   - **Metric:** `ecommerce_cart_additions_total` incremented
   - **Trace:** Full request trace including DB query time

---

## 📁 Project Structure
```
E-commerce/
├── app/
│   ├── __init__.py              # App initialization, config, observability setup
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py              # User model with password hashing
│   │   ├── product.py           # Product model
│   │   ├── cart.py              # Cart and CartItem models
│   │   └── order.py             # Order and OrderItem models
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── users.py             # User registration/login endpoints
│   │   ├── products.py          # Product CRUD endpoints
│   │   ├── cart.py              # Cart management endpoints
│   │   ├── orders.py            # Order creation/viewing endpoints
│   │   └── admin.py             # Admin dashboard endpoints
│   ├── services/
│   │   ├── user_service.py      # User business logic
│   │   ├── product_service.py   # Product business logic
│   │   ├── cart_service.py      # Cart business logic
│   │   └── order_service.py     # Order business logic
│   └── metrics.py               # Custom metrics definitions
├── static/
│   ├── index.html               # Main frontend page
│   ├── admin.html               # Admin dashboard page
│   ├── app.js                   # Main frontend JavaScript
│   ├── admin.js                 # Admin dashboard JavaScript
│   ├── style.css                # Styles for main page
│   └── images/                  # Product images
├── instance/
│   └── ecommerce.db             # SQLite database (auto-created)
├── .env                         # Environment variables
├── .gitignore                   # Git ignore file
├── requirements.txt             # Python dependencies
├── run.py                       # Application entry point
├── add_sample_data.py           # Script to populate sample products
├── create_admin.py              # Script to create admin user
├── app.log                      # Application logs (auto-created)
└── README.md                    # This file
```

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git (for cloning)

### Step 1: Clone the Repository
```bash
git clone https://github.com/ArcTucruz/ecommerce-observability.git
cd ecommerce-observability
```

### Step 2: Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

**Required Packages:**
- Flask
- Flask-SQLAlchemy
- Flask-CORS
- Werkzeug
- python-dotenv
- prometheus-flask-exporter
- opentelemetry-api
- opentelemetry-sdk
- opentelemetry-instrumentation-flask
- opentelemetry-instrumentation-sqlalchemy

### Step 4: Configure Environment

The `.env` file should already exist with:
```
DATABASE_TYPE=sqlite
SQLITE_DB_PATH=ecommerce.db
SECRET_KEY=your-secret-key-change-this-in-production
FLASK_ENV=development
PORT=5000
LOG_LEVEL=INFO
DEBUG_METRICS=1
```

### Step 5: Initialize Database & Add Data
```bash
# The database will be created automatically when you first run the app
# Add sample products
python add_sample_data.py

# Create admin user (username: admin, password: admin123)
python create_admin.py
```

### Step 6: Run the Application
```bash
python run.py
```

**Application will be available at:**
- **Main Store:** http://localhost:5000
- **Admin Dashboard:** http://localhost:5000/admin.html
- **Metrics Endpoint:** http://localhost:5000/metrics
- **Health Check:** http://localhost:5000/health

---

## 🔌 API Endpoints

### User Authentication
- **POST** `/api/users/register` - Register new user
- **POST** `/api/users/login` - User login
- **GET** `/api/users/<user_id>` - Get user by ID

### Products
- **GET** `/api/products` - Get all products
- **GET** `/api/products/<product_id>` - Get product by ID

### Shopping Cart
- **POST** `/api/cart/add` - Add item to cart
- **DELETE** `/api/cart/remove/<cart_item_id>` - Remove item from cart
- **GET** `/api/cart/<user_id>` - Get user's cart
- **PUT** `/api/cart/update/<cart_item_id>` - Update item quantity

### Orders
- **POST** `/api/orders` - Create new order
- **GET** `/api/orders/<user_id>` - Get user's orders
- **GET** `/api/orders/<order_id>/details` - Get order details

### Admin (Admin only)
- **GET** `/api/admin/stats` - Get dashboard statistics
- **GET** `/api/admin/users` - Get all users
- **GET** `/api/admin/orders` - Get all orders
- **POST** `/api/admin/products` - Create new product
- **PUT** `/api/admin/products/<product_id>` - Update product
- **DELETE** `/api/admin/products/<product_id>` - Delete product

### Observability
- **GET** `/metrics` - Prometheus metrics endpoint
- **GET** `/health` - Health check endpoint

---

## 📖 Usage

### For Regular Users

1. **Browse Products**
   - Open http://localhost:5000
   - Click "Products" to view catalog

2. **Register/Login**
   - Click "Register" to create account
   - Or "Login" if you already have an account

3. **Shopping**
   - Add products to cart
   - View cart with totals
   - Proceed to checkout
   - Enter shipping details
   - Place order

4. **View Orders**
   - Click "My Orders" to see order history

### For Administrators

1. **Login as Admin**
   - Username: `admin`
   - Password: `admin123`

2. **Access Admin Panel**
   - Click "Admin Panel" button (appears only for admins)

3. **Dashboard Features**
   - View statistics (users, products, orders, revenue)
   - Manage users (view, export)
   - Manage products (add, edit, delete, export)
   - Manage orders (view, export)

4. **Add New Product**
   - Click "Add Product" button
   - Fill in product details
   - Submit form

5. **Export Data**
   - Click "Export CSV" on any table
   - Download data as CSV file

### Monitoring & Observability

1. **View Logs**
```bash
   # View logs in real-time
   tail -f app.log
   
   # Or on Windows
   Get-Content app.log -Wait
```

2. **Check Metrics**
   - Open http://localhost:5000/metrics
   - View Prometheus-compatible metrics
   - Use with Prometheus + Grafana for visualization

3. **Health Check**
   - Open http://localhost:5000/health
   - Returns JSON with app status

---

## 📊 Observability Dashboard (Grafana)

This application is ready for monitoring with Prometheus and Grafana:

1. **Prometheus** scrapes `/metrics` endpoint every 15 seconds
2. **Grafana** visualizes metrics with dashboards:
   - User registration trends
   - Login success/failure rates
   - Cart activity
   - Order volumes
   - Revenue tracking
   - System performance (request latency, error rates)

*Dashboard configurations can be found in the monitoring setup guide.*

---

## 🎯 Key Learning Points

This project demonstrates:

1. **Full-Stack Development**
   - RESTful API design
   - Frontend-backend communication
   - State management

2. **Observability Best Practices**
   - Structured logging
   - Metrics collection
   - Distributed tracing
   - The three pillars in action

3. **Security**
   - Password hashing
   - Input validation
   - SQL injection prevention (via ORM)

4. **Software Architecture**
   - Separation of concerns (Routes → Services → Models)
   - Modular design
   - Scalable structure

---

## 👨‍💻 Author

**Irfan Yuliana Putra**
- GitHub: [@ArcTucruz](https://github.com/ArcTucruz)

---

## 📝 License

This project is created for educational and demonstration purposes.

---

## 🙏 Acknowledgments

- Flask documentation
- Prometheus documentation
- OpenTelemetry documentation
- Observability best practices from industry leaders

---

**Happy Monitoring! 📊🚀**