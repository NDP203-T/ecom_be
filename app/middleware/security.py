from flask import request, jsonify
from functools import wraps

def validate_content_type(content_types=['application/json']):
    """Validate request content type"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if request.method in ['POST', 'PUT', 'PATCH']:
                if 'multipart/form-data' not in request.content_type:
                    if request.content_type not in content_types:
                        return jsonify({'error': 'Invalid content type'}), 400
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def register_middleware(app):
    """Register security middleware"""
    
    @app.before_request
    def security_headers():
        """Add security headers to all responses"""
        pass
    
    @app.after_request
    def add_security_headers(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        return response
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500
