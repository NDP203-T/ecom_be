from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.controllers.category_controller import CategoryController
from app.middleware.auth import admin_required
from app.middleware.validation import validate_json
from app.middleware.encryption import encrypt_response

bp = Blueprint('category', __name__, url_prefix='/api/categories')

@bp.route('', methods=['GET'])
@encrypt_response()
def get_all_categories():
    """Lấy danh sách danh mục (Public)"""
    include_children = request.args.get('include_children', 'false').lower() == 'true'
    only_parents = request.args.get('only_parents', 'false').lower() == 'true'
    is_active = request.args.get('is_active', None)
    
    result, status_code = CategoryController.get_all_categories(
        include_children=include_children,
        only_parents=only_parents,
        is_active=is_active
    )
    return jsonify(result), status_code

@bp.route('/tree', methods=['GET'])
@encrypt_response()
def get_category_tree():
    """Lấy cây danh mục phân cấp (Public)"""
    result, status_code = CategoryController.get_category_tree()
    return jsonify(result), status_code

@bp.route('/<category_id>', methods=['GET'])
@encrypt_response()
def get_category(category_id):
    """Lấy chi tiết danh mục (Public)"""
    include_children = request.args.get('include_children', 'true').lower() == 'true'
    result, status_code = CategoryController.get_category_by_id(category_id, include_children)
    return jsonify(result), status_code

@bp.route('/slug/<slug>', methods=['GET'])
@encrypt_response()
def get_category_by_slug(slug):
    """Lấy danh mục theo slug (Public)"""
    include_children = request.args.get('include_children', 'true').lower() == 'true'
    result, status_code = CategoryController.get_category_by_slug(slug, include_children)
    return jsonify(result), status_code

@bp.route('/add', methods=['POST'])
@jwt_required()
@admin_required
@validate_json('name', 'slug')
@encrypt_response()
def create_category():
    """Tạo danh mục mới (Admin only)"""
    data = request.get_json()
    result, status_code = CategoryController.create_category(data)
    return jsonify(result), status_code

@bp.route('/<category_id>', methods=['PUT'])
@jwt_required()
@admin_required
@encrypt_response()
def update_category(category_id):
    """Cập nhật danh mục (Admin only)"""
    data = request.get_json()
    result, status_code = CategoryController.update_category(category_id, data)
    return jsonify(result), status_code

@bp.route('/<category_id>', methods=['DELETE'])
@jwt_required()
@admin_required
@encrypt_response()
def delete_category(category_id):
    """Xóa danh mục (Admin only)"""
    result, status_code = CategoryController.delete_category(category_id)
    return jsonify(result), status_code

@bp.route('/<category_id>/toggle-status', methods=['PUT'])
@jwt_required()
@admin_required
@encrypt_response()
def toggle_category_status(category_id):
    """Ẩn/hiện danh mục (Admin only)"""
    result, status_code = CategoryController.toggle_category_status(category_id)
    return jsonify(result), status_code
