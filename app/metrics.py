"""
Prometheus Metrics for E-commerce Application
Tracks: Requests, Errors, Response Times, Business Metrics
"""
import logging
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import Counter, Histogram, Gauge

logger = logging.getLogger(__name__)

# Custom business metrics
user_registrations = Counter(
    'ecommerce_user_registrations_total',
    'Total number of user registrations'
)

user_logins = Counter(
    'ecommerce_user_logins_total',
    'Total number of login attempts',
    ['status']  # success or failure
)

products_added_to_cart = Counter(
    'ecommerce_cart_additions_total',
    'Total number of products added to cart'
)

orders_created = Counter(
    'ecommerce_orders_total',
    'Total number of orders created'
)

order_value = Histogram(
    'ecommerce_order_value_dollars',
    'Order value in dollars',
    buckets=[10, 50, 100, 500, 1000, 5000]
)

active_users = Gauge(
    'ecommerce_active_users',
    'Number of currently active users'
)

def init_metrics(app):
    """
    Initialize Prometheus metrics for the application
    """
    # This automatically creates /metrics endpoint
    # and tracks basic HTTP metrics
    metrics = PrometheusMetrics(app)
    
    # Track specific endpoints
    metrics.info('ecommerce_app_info', 'E-commerce Application Info', version='1.0.0')
    
    logger.info("✅ Prometheus metrics initialized at /metrics")
    
    return metrics

def record_user_registration():
    """Record a new user registration"""
    user_registrations.inc()

def record_login(success=True):
    """Record a login attempt"""
    status = 'success' if success else 'failure'
    user_logins.labels(status=status).inc()

def record_cart_addition():
    """Record product added to cart"""
    products_added_to_cart.inc()

def record_order(total_amount):
    """Record a new order"""
    orders_created.inc()
    order_value.observe(total_amount)

def update_active_users(count):
    """Update active users count"""
    active_users.set(count)