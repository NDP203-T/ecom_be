import requests
from flask import current_app
from app import db
from app.models import User
import logging

logger = logging.getLogger(__name__)

class GoogleOAuthService:
    
    @staticmethod
    def verify_google_token(token):
        """Xác thực Google ID token"""
        try:
            # Gọi Google API để verify token
            response = requests.get(
                'https://oauth2.googleapis.com/tokeninfo',
                params={'id_token': token}
            )
            
            if response.status_code != 200:
                logger.error(f"Google token verification failed: {response.text}")
                return None
            
            user_info = response.json()
            
            # Kiểm tra client_id
            if user_info.get('aud') != current_app.config['GOOGLE_CLIENT_ID']:
                logger.error("Invalid Google client ID")
                return None
            
            return user_info
            
        except Exception as e:
            logger.error(f"Error verifying Google token: {str(e)}")
            return None
    
    @staticmethod
    def get_or_create_user(user_info):
        """Tạo hoặc lấy user từ Google info"""
        email = user_info.get('email')
        google_id = user_info.get('sub')
        
        if not email:
            return None
        
        # Tìm user theo email
        user = User.query.filter_by(email=email.lower()).first()
        
        if user:
            # User đã tồn tại, cập nhật thông tin OAuth nếu chưa có
            if not user.oauth_provider:
                user.oauth_provider = 'google'
                user.oauth_id = google_id
                user.is_verified = True  # Google đã verify email
                
                if user_info.get('picture'):
                    user.avatar_url = user_info.get('picture')
                
                db.session.commit()
            
            return user
        
        # Tạo user mới
        user = User(
            email=email.lower(),
            full_name=user_info.get('name'),
            oauth_provider='google',
            oauth_id=google_id,
            avatar_url=user_info.get('picture'),
            is_verified=True,  # Google đã verify email
            is_active=True
        )
        
        db.session.add(user)
        db.session.commit()
        
        logger.info(f"New user created via Google OAuth: {email}")
        
        return user
