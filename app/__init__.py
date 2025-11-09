import os
import logging
import logging.config
import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize SQLAlchemy
db = SQLAlchemy()

# Setup logging - COMPLETE VERSION
# Remove all existing handlers
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

# Create file handler with immediate flush
file_handler = logging.FileHandler('app.log', mode='a', encoding='utf-8')
file_handler.setLevel(logging.DEBUG)
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)

# Create console handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_formatter)

# Configure root logger
root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)
root_logger.addHandler(file_handler)
root_logger.addHandler(console_handler)

# Make sure app loggers work
logging.getLogger('app').setLevel(logging.DEBUG)
logging.getLogger('app.services').setLevel(logging.DEBUG)
logging.getLogger('app.services.user_service').setLevel(logging.DEBUG)
logging.getLogger('app.services.cart_service').setLevel(logging.DEBUG)
logging.getLogger('app.services.product_service').setLevel(logging.DEBUG)
logging.getLogger('app.services.order_service').setLevel(logging.DEBUG)

# Reduce Flask noise
logging.getLogger('werkzeug').setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

def get_database_uri():
    """
    Get database URI based on DATABASE_TYPE in .env file
    """
    db_type = os.getenv('DATABASE_TYPE', 'sqlite').lower()
    
    if db_type == 'sqlite':
        db_path = os.getenv('SQLITE_DB_PATH', 'ecommerce.db')
        return f'sqlite:///{db_path}'
    
    elif db_type == 'mysql':
        host = os.getenv('MYSQL_HOST', 'localhost')
        port = os.getenv('MYSQL_PORT', '3306')
        user = os.getenv('MYSQL_USER', 'root')
        password = os.getenv('MYSQL_PASSWORD', '')
        database = os.getenv('MYSQL_DATABASE', 'ecommerce_db')
        return f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}'
    
    else:
        return 'sqlite:///ecommerce.db'

def create_app():
    """
    Application factory - creates and configures Flask app with monitoring
    """
    logger.info("Logging system initialized")
    
    # Create Flask app
    app = Flask(__name__, static_folder='../static', static_url_path='/static')
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = get_database_uri()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    logger.info(f"Database configured: {app.config['SQLALCHEMY_DATABASE_URI'].split('://')[0]}")
    
    # Initialize extensions
    db.init_app(app)
    CORS(app)
    
    # Initialize Prometheus Metrics
    try:
        from app.metrics import init_metrics
        init_metrics(app)
    except Exception as e:
        logger.warning(f"⚠️ Could not initialize metrics: {e}")
    
    # Initialize OpenTelemetry Tracing
    try:
        from app.tracing import init_tracing
        with app.app_context():
            init_tracing(app, db.engine)
    except Exception as e:
        logger.warning(f"⚠️ Could not initialize tracing: {e}")
    
    # Register blueprints (API routes)
    from app.routes import products, cart, orders, users, admin
    
    app.register_blueprint(products.bp)
    app.register_blueprint(cart.bp)
    app.register_blueprint(orders.bp)
    app.register_blueprint(users.bp)
    app.register_blueprint(admin.bp)
    
    logger.info("API routes registered successfully")
    
    # Serve frontend
    @app.route('/')
    def index():
        return app.send_static_file('index.html')
    
    # Serve admin page
    @app.route('/admin.html')
    def admin_page():
        return app.send_static_file('admin.html')
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        return {'status': 'healthy', 'service': 'ecommerce-api'}, 200
    
    # Create database tables
    with app.app_context():
        db.create_all()
        logger.info("Database tables created successfully")
    
    return app