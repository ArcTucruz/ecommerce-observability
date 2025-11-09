import logging
from flask import Blueprint, request, jsonify
from app.services.user_service import UserService

logger = logging.getLogger(__name__)

bp = Blueprint('users', __name__, url_prefix='/api/users')

@bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json()
        
        if not all(field in data for field in ['username', 'email', 'password']):
            return jsonify({'error': 'Missing required fields'}), 400
        
        user, error = UserService.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            full_name=data.get('full_name')
        )
        
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({
            'message': 'User registered successfully',
            'user': user.to_dict()
        }), 201
        
    except Exception as e:
        logger.error(f"Error in register: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/login', methods=['POST'])
def login():
    """Login user"""
    try:
        data = request.get_json()
        
        if 'username' not in data or 'password' not in data:
            return jsonify({'error': 'Missing credentials'}), 400
        
        user, error = UserService.authenticate_user(
            username=data['username'],
            password=data['password']
        )
        
        if error:
            return jsonify({'error': error}), 401
        
        return jsonify({
            'message': 'Login successful',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        logger.error(f"Error in login: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get user by ID"""
    try:
        user, error = UserService.get_user_by_id(user_id)
        
        if error:
            return jsonify({'error': error}), 404
        
        return jsonify(user.to_dict()), 200
        
    except Exception as e:
        logger.error(f"Error in get_user: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500