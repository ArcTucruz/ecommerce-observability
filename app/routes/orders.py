import logging
from flask import Blueprint, request, jsonify
from app.services.order_service import OrderService

logger = logging.getLogger(__name__)

bp = Blueprint('orders', __name__, url_prefix='/api/orders')

@bp.route('', methods=['POST'])
def create_order():
    """Create an order from cart"""
    try:
        data = request.get_json()
        
        if 'user_id' not in data or 'shipping_address' not in data:
            return jsonify({'error': 'Missing required fields'}), 400
        
        order, error = OrderService.create_order(
            user_id=data['user_id'],
            shipping_address=data['shipping_address'],
            payment_method=data.get('payment_method', 'credit_card')
        )
        
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({
            'message': 'Order created successfully',
            'order': order.to_dict()
        }), 201
        
    except Exception as e:
        logger.error(f"Error in create_order: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/user/<int:user_id>', methods=['GET'])
def get_user_orders(user_id):
    """Get all orders for a user"""
    try:
        orders, error = OrderService.get_user_orders(user_id)
        
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({
            'orders': [order.to_dict() for order in orders],
            'count': len(orders)
        }), 200
        
    except Exception as e:
        logger.error(f"Error in get_user_orders: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


#**What this does:**
#- `POST /api/orders` - Create order from cart
#- `GET /api/orders/user/<user_id>` - Get user's orders

## ✅ Routes Complete!

#app/
#└── routes/
#    ├── __init__.py         ✅
#    ├── users.py           ✅ (Register, Login)
#    ├── products.py        ✅ (Get products, Create)
#    ├── cart.py            ✅ (Cart operations)
#    └── orders.py          ✅ (Create order, View orders)