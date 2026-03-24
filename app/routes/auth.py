from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.controllers.auth_controller import AuthController
from app.middleware.validation import validate_json
from app.middleware.encryption import encrypt_response

bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@bp.route('/register', methods=['POST'])
@validate_json('email', 'password')
@encrypt_response()
def register():
    data = request.get_json()
    result, status_code = AuthController.register(data)
    return jsonify(result), status_code

@bp.route('/verify-otp', methods=['POST'])
@validate_json('email', 'code')
@encrypt_response()
def verify_otp():
    data = request.get_json()
    result, status_code = AuthController.verify_otp(data)
    return jsonify(result), status_code

@bp.route('/resend-otp', methods=['POST'])
@validate_json('email')
@encrypt_response()
def resend_otp():
    data = request.get_json()
    result, status_code = AuthController.resend_otp(data)
    return jsonify(result), status_code

@bp.route('/login', methods=['POST'])
@validate_json('email', 'password')
@encrypt_response()
def login():
    data = request.get_json()
    result, status_code = AuthController.login(data)
    return jsonify(result), status_code

@bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
@encrypt_response()
def refresh():
    user_id = get_jwt_identity()
    result, status_code = AuthController.refresh_token(user_id)
    return jsonify(result), status_code


@bp.route('/google', methods=['POST'])
@validate_json('token')
@encrypt_response()
def google_login():
    """Đăng nhập bằng Google"""
    data = request.get_json()
    result, status_code = AuthController.google_login(data)
    return jsonify(result), status_code
