from app import db
from app.models import User

class UserService:
    
    @staticmethod
    def get_all_users(page=1, per_page=10):
        """Lấy danh sách tất cả user với phân trang"""
        pagination = User.query.order_by(User.created_at.desc()).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        return pagination.items, pagination.total
    
    @staticmethod
    def get_user_by_id(user_id):
        """Lấy user theo ID"""
        return User.query.get(user_id)
    
    @staticmethod
    def toggle_user_status(user_id):
        """Khóa/mở tài khoản user"""
        user = User.query.get(user_id)
        if user:
            user.is_active = not user.is_active
            db.session.commit()
            return user.is_active
        return None
    
    @staticmethod
    def update_user_role(user_id, new_role):
        """Cập nhật role cho user"""
        user = User.query.get(user_id)
        if user:
            user.role = new_role
            db.session.commit()
            return user
        return None
    
    @staticmethod
    def reset_password(user_id, new_password):
        """Reset mật khẩu cho user"""
        user = User.query.get(user_id)
        if user:
            user.set_password(new_password)
            db.session.commit()
            return user
        return None
