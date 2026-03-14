from flask_jwt_extended import create_access_token, create_refresh_token
from datetime import timedelta
from app import db
from app.models import User

class AuthService:
    
    @staticmethod
    def create_user(email, password, full_name=None):
        """Tạo user mới"""
        user = User(
            email=email.lower().strip(),
            full_name=full_name.strip() if full_name else None
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        return user
    
    @staticmethod
    def find_user_by_email(email):
        """Tìm user theo email"""
        return User.query.filter_by(email=email.lower().strip()).first()
    
    @staticmethod
    def verify_password(user, password):
        """Kiểm tra password"""
        return user.check_password(password)
    
    @staticmethod
    def generate_tokens(user_id):
        """Tạo access token và refresh token"""
        access_token = create_access_token(
            identity=user_id,
            expires_delta=timedelta(hours=1)
        )
        refresh_token = create_refresh_token(
            identity=user_id,
            expires_delta=timedelta(days=30)
        )
        return access_token, refresh_token
