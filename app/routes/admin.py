import logging
from flask import Blueprint, request, jsonify
from app import db
from app.models.user import User
from app.models.product import Product
from app.models.order import Order

logger = logging.getLogger(__name__)

bp = Blueprint('admin', __name__, url_prefix='/api/admin')

def check_admin(user_id):
    """Helper function to check if user is admin"""
    user = User.query.get(user_id)
    if not user or not user.is_admin:
        return False
    return True

@bp.route('/users', methods=['GET'])
def get_all_users():
    """Get all users (admin only)"""
    try:
        # In a real app, this is where we check authentication 
        # For demo, we'll just return data
        
        users = User.query.all()
        logger.info(f"📊 Admin viewed all users (Total: {len(users)})")
        
        return jsonify({
            'users': [user.to_dict() for user in users],
            'count': len(users)
        }), 200
        
    except Exception as e:
        logger.error(f"❌ Error fetching users: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/orders', methods=['GET'])
def get_all_orders():
    """Get all orders (admin only)"""
    try:
        orders = Order.query.order_by(Order.created_at.desc()).all()
        logger.info(f"📊 Admin viewed all orders (Total: {len(orders)})")
        
        return jsonify({
            'orders': [order.to_dict() for order in orders],
            'count': len(orders)
        }), 200
        
    except Exception as e:
        logger.error(f"❌ Error fetching orders: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/stats', methods=['GET'])
def get_stats():
    """Get admin dashboard statistics"""
    try:
        total_users = User.query.count()
        total_products = Product.query.count()
        total_orders = Order.query.count()
        total_revenue = db.session.query(db.func.sum(Order.total_amount)).scalar() or 0
        
        logger.info("📊 Admin viewed dashboard statistics")
        
        return jsonify({
            'total_users': total_users,
            'total_products': total_products,
            'total_orders': total_orders,
            'total_revenue': float(total_revenue)
        }), 200
        
    except Exception as e:
        logger.error(f"❌ Error fetching stats: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    """Update product (admin only)"""
    try:
        data = request.get_json()
        product = Product.query.get(product_id)
        
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        # Update fields
        if 'name' in data:
            product.name = data['name']
        if 'price' in data:
            product.price = data['price']
        if 'description' in data:
            product.description = data['description']
        if 'stock_quantity' in data:
            product.stock_quantity = data['stock_quantity']
        if 'category' in data:
            product.category = data['category']
        
        db.session.commit()
        
        logger.info(f"✅ Admin updated product: {product.name}")
        
        return jsonify({
            'message': 'Product updated successfully',
            'product': product.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"❌ Error updating product: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    """Delete product (admin only)"""
    try:
        product = Product.query.get(product_id)
        
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        product_name = product.name
        db.session.delete(product)
        db.session.commit()
        
        logger.info(f"✅ Admin deleted product: {product_name}")
        
        return jsonify({'message': 'Product deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"❌ Error deleting product: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/products', methods=['POST'])
def create_product():
    """Create new product (admin only)"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'price', 'description', 'stock_quantity', 'category']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Create new product
        product = Product(
            name=data['name'],
            price=float(data['price']),
            description=data['description'],
            stock_quantity=int(data['stock_quantity']),
            category=data['category'],
            image_url=data.get('image_url', '/static/images/default-product.jpg')
        )
        
        db.session.add(product)
        db.session.commit()
        
        logger.info(f"✅ Admin created new product: {product.name} (Price: ${product.price}, Stock: {product.stock_quantity})")
        
        return jsonify({
            'message': 'Product created successfully',
            'product': product.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"❌ Error creating product: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500