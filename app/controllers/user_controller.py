from app.services.user_service import UserService
from app.models import User
import logging

logger = logging.getLogger(__name__)

class UserController:
    
    @staticmethod
    def get_all_users(page=1, per_page=10):
        """Lấy danh sách tất cả user với phân trang"""
        users, total = UserService.get_all_users(page, per_page)
        
        return {
            'users': [user.to_dict() for user in users],
            'total': total,
            'page': page,
            'per_page': per_page,
            'total_pages': (total + per_page - 1) // per_page
        }, 200
    
    @staticmethod
    def get_user_by_id(user_id):
        """Lấy thông tin user theo ID"""
        user = UserService.get_user_by_id(user_id)
        
        if not user:
            return {'error': 'User not found'}, 404
        
        return {'user': user.to_dict()}, 200
    
    @staticmethod
    def toggle_user_status(user_id, admin_id):
        """Khóa/mở tài khoản user"""
        # Không cho phép tự khóa chính mình
        if user_id == admin_id:
            return {'error': 'Cannot lock/unlock your own account'}, 400
        
        user = UserService.get_user_by_id(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        
        # Toggle trạng thái
        new_status = UserService.toggle_user_status(user_id)
        
        return {
            'message': f'User {"locked" if not new_status else "unlocked"} successfully',
            'user': user.to_dict()
        }, 200
    
    @staticmethod
    def update_user_role(user_id, new_role, admin_id):
        """Phân quyền cho user (ADMIN/USER)"""
        # Không cho phép tự thay đổi quyền của chính mình
        if user_id == admin_id:
            return {'error': 'Cannot change your own role'}, 400
        
        # Validate role
        if new_role.upper() not in ['ADMIN', 'USER']:
            return {'error': 'Invalid role. Must be ADMIN or USER'}, 400
        
        user = UserService.get_user_by_id(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        
        # Cập nhật role
        UserService.update_user_role(user_id, new_role.lower())
        
        return {
            'message': f'User role updated to {new_role.upper()} successfully',
            'user': user.to_dict()
        }, 200
    
    @staticmethod
    def reset_user_password(user_id, new_password):
        """Reset mật khẩu cho user"""
        # Validate password
        if len(new_password) < 6:
            return {'error': 'Password must be at least 6 characters'}, 400
        
        user = UserService.get_user_by_id(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        
        # Reset password
        UserService.reset_password(user_id, new_password)
        
        logger.info(f"Password reset for user {user.email} by admin")
        
        return {
            'message': 'Password reset successfully',
            'user': user.to_dict()
        }, 200
