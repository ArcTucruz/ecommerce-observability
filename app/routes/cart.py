import logging
from flask import Blueprint, request, jsonify
from app.services.cart_service import CartService

logger = logging.getLogger(__name__)

bp = Blueprint('cart', __name__, url_prefix='/api/cart')

@bp.route('/<int:user_id>', methods=['GET'])
def get_cart(user_id):
    """Get user's cart"""
    try:
        cart, error = CartService.get_cart(user_id)
        
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify(cart.to_dict()), 200
        
    except Exception as e:
        logger.error(f"Error in get_cart: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/<int:user_id>/add', methods=['POST'])
def add_to_cart(user_id):
    """Add product to cart"""
    try:
        data = request.get_json()
        
        if 'product_id' not in data:
            return jsonify({'error': 'Missing product_id'}), 400
        
        quantity = data.get('quantity', 1)
        
        cart, error = CartService.add_to_cart(user_id, data['product_id'], quantity)
        
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({
            'message': 'Product added to cart',
            'cart': cart.to_dict()
        }), 200
        
    except Exception as e:
        logger.error(f"Error in add_to_cart: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/<int:user_id>/remove/<int:product_id>', methods=['DELETE'])
def remove_from_cart(user_id, product_id):
    """Remove product from cart"""
    try:
        cart, error = CartService.remove_from_cart(user_id, product_id)
        
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({
            'message': 'Product removed from cart',
            'cart': cart.to_dict()
        }), 200
        
    except Exception as e:
        logger.error(f"Error in remove_from_cart: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500