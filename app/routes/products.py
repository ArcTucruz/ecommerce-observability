import logging
from flask import Blueprint, request, jsonify
from app.services.product_service import ProductService

logger = logging.getLogger(__name__)

bp = Blueprint('products', __name__, url_prefix='/api/products')

@bp.route('', methods=['GET'])
def get_products():
    """Get all products"""
    try:
        products, error = ProductService.get_all_products()
        
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({
            'products': [product.to_dict() for product in products],
            'count': len(products)
        }), 200
        
    except Exception as e:
        logger.error(f"Error in get_products: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Get product by ID"""
    try:
        product, error = ProductService.get_product_by_id(product_id)
        
        if error:
            return jsonify({'error': error}), 404
        
        return jsonify(product.to_dict()), 200
        
    except Exception as e:
        logger.error(f"Error in get_product: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('', methods=['POST'])
def create_product():
    """Create a new product"""
    try:
        data = request.get_json()
        
        if 'name' not in data or 'price' not in data:
            return jsonify({'error': 'Missing required fields'}), 400
        
        product, error = ProductService.create_product(
            name=data['name'],
            price=data['price'],
            description=data.get('description'),
            stock_quantity=data.get('stock_quantity', 0),
            category=data.get('category')
        )
        
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({
            'message': 'Product created successfully',
            'product': product.to_dict()
        }), 201
        
    except Exception as e:
        logger.error(f"Error in create_product: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500