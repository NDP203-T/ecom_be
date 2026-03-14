from flask import request, jsonify
from functools import wraps

def validate_json(*expected_args):
    """Validate JSON request body"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not request.is_json:
                return jsonify({'error': 'Content-Type must be application/json'}), 400
            
            json_data = request.get_json()
            if not json_data:
                return jsonify({'error': 'Invalid JSON'}), 400
            
            missing_fields = [field for field in expected_args if field not in json_data]
            if missing_fields:
                return jsonify({'error': f'Missing fields: {", ".join(missing_fields)}'}), 400
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def validate_file_upload(allowed_extensions={'png', 'jpg', 'jpeg', 'gif', 'webp'}):
    """Validate file upload"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'file' not in request.files and 'image' not in request.files:
                return jsonify({'error': 'No file uploaded'}), 400
            
            file = request.files.get('file') or request.files.get('image')
            
            if file.filename == '':
                return jsonify({'error': 'No file selected'}), 400
            
            if not allowed_file(file.filename, allowed_extensions):
                return jsonify({'error': f'Invalid file type. Allowed: {", ".join(allowed_extensions)}'}), 400
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions
