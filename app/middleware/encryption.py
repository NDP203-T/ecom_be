from flask import request, jsonify
from functools import wraps
from app.utils.encryption import EncryptionUtil

def encrypt_response(exclude_keys=None):
    """
    Decorator để mã hóa values trong response, giữ nguyên keys
    exclude_keys: list các keys không cần mã hóa (vd: ['message', 'encrypted'])
    """
    if exclude_keys is None:
        exclude_keys = ['message', 'error']
    
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Gọi function gốc
            response = f(*args, **kwargs)
            
            # Lấy data từ response
            if isinstance(response, tuple):
                data, status_code = response[0], response[1]
            else:
                data, status_code = response, 200
            
            # Lấy JSON data
            if hasattr(data, 'get_json'):
                json_data = data.get_json()
            elif hasattr(data, 'json'):
                json_data = data.json
            else:
                json_data = data
            
            # Mã hóa values, giữ nguyên keys
            encrypted_data = EncryptionUtil.encrypt_dict(json_data, exclude_keys)
            encrypted_data['encrypted'] = True
            
            return jsonify(encrypted_data), status_code
        
        return decorated_function
    return decorator
