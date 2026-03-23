from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from functools import wraps
from app.models import User

def admin_required(fn):
    """Require admin role"""
    @wraps(fn)
    def decorator(*args, **kwargs):
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        if not user.is_active:
            return jsonify({'error': 'Account is locked'}), 403
        
        if user.role != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        
        return fn(*args, **kwargs)
    return decorator

def user_required(fn):
    """Require user role (user hoặc admin)"""
    @wraps(fn)
    def decorator(*args, **kwargs):
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        if not user.is_active:
            return jsonify({'error': 'Account is locked'}), 403
        
        if not user.is_verified:
            return jsonify({'error': 'Email not verified'}), 403
        
        return fn(*args, **kwargs)
    return decorator
