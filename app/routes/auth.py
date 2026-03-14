from flask import Blueprint, request, jsonify
from app.controllers.auth_controller import AuthController
from app.middleware.validation import validate_json

bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@bp.route('/register', methods=['POST'])
@validate_json('email', 'password')
def register():
    data = request.get_json()
    result, status_code = AuthController.register(data)
    return jsonify(result), status_code

@bp.route('/verify-otp', methods=['POST'])
@validate_json('email', 'code')
def verify_otp():
    data = request.get_json()
    result, status_code = AuthController.verify_otp(data)
    return jsonify(result), status_code

@bp.route('/resend-otp', methods=['POST'])
@validate_json('email')
def resend_otp():
    data = request.get_json()
    result, status_code = AuthController.resend_otp(data)
    return jsonify(result), status_code

@bp.route('/login', methods=['POST'])
@validate_json('email', 'password')
def login():
    data = request.get_json()
    result, status_code = AuthController.login(data)
    return jsonify(result), status_code
