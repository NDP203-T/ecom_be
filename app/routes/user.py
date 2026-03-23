from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.controllers.user_controller import UserController
from app.middleware.auth import admin_required
from app.middleware.validation import validate_json
from app.middleware.encryption import encrypt_response

bp = Blueprint('user', __name__, url_prefix='/api/users')

@bp.route('', methods=['GET'])
@jwt_required()
@admin_required
@encrypt_response()
def get_all_users():
    """Lấy danh sách tất cả user (chỉ ADMIN)"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    result, status_code = UserController.get_all_users(page, per_page)
    return jsonify(result), status_code

@bp.route('/<user_id>', methods=['GET'])
@jwt_required()
@admin_required
@encrypt_response()
def get_user(user_id):
    """Lấy thông tin user theo ID (chỉ ADMIN)"""
    result, status_code = UserController.get_user_by_id(user_id)
    return jsonify(result), status_code

@bp.route('/<user_id>/toggle-status', methods=['PUT'])
@jwt_required()
@admin_required
@encrypt_response()
def toggle_user_status(user_id):
    """Khóa/mở tài khoản user (chỉ ADMIN)"""
    admin_id = get_jwt_identity()
    result, status_code = UserController.toggle_user_status(user_id, admin_id)
    return jsonify(result), status_code

@bp.route('/<user_id>/role', methods=['PUT'])
@jwt_required()
@admin_required
@validate_json('role')
@encrypt_response()
def update_user_role(user_id):
    """Phân quyền cho user (chỉ ADMIN)"""
    admin_id = get_jwt_identity()
    data = request.get_json()
    new_role = data.get('role')
    
    result, status_code = UserController.update_user_role(user_id, new_role, admin_id)
    return jsonify(result), status_code

@bp.route('/<user_id>/reset-password', methods=['PUT'])
@jwt_required()
@admin_required
@validate_json('new_password')
@encrypt_response()
def reset_password(user_id):
    """Reset mật khẩu cho user (chỉ ADMIN)"""
    data = request.get_json()
    new_password = data.get('new_password')
    
    result, status_code = UserController.reset_user_password(user_id, new_password)
    return jsonify(result), status_code
