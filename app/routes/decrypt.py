from flask import Blueprint, request, jsonify
from app.utils.encryption import EncryptionUtil

bp = Blueprint('decrypt', __name__, url_prefix='/api/decrypt')

@bp.route('/test', methods=['POST'])
def decrypt_test():
    """API để test giải mã - dùng trong Swagger"""
    data = request.get_json()
    
    if not data or 'encrypted_value' not in data:
        return jsonify({'error': 'Missing encrypted_value'}), 400
    
    decrypted = EncryptionUtil.decrypt_value(data['encrypted_value'])
    
    return jsonify({
        'decrypted': decrypted
    }), 200

@bp.route('/response', methods=['POST'])
def decrypt_response():
    """API để giải mã toàn bộ response"""
    data = request.get_json()
    
    if not data or 'response' not in data:
        return jsonify({'error': 'Missing response data'}), 400
    
    response_data = data['response']
    
    def decrypt_dict(obj):
        if isinstance(obj, dict):
            result = {}
            for key, value in obj.items():
                if key in ['encrypted', 'message', 'error']:
                    result[key] = value
                elif isinstance(value, dict):
                    result[key] = decrypt_dict(value)
                elif isinstance(value, list):
                    result[key] = [decrypt_dict(item) if isinstance(item, dict) else EncryptionUtil.decrypt_value(item) for item in value]
                else:
                    result[key] = EncryptionUtil.decrypt_value(value)
            return result
        return obj
    
    decrypted = decrypt_dict(response_data)
    
    return jsonify(decrypted), 200
