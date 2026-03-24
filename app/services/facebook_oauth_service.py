import requests
from flask import current_app
from app import db
from app.models import User
import logging

logger = logging.getLogger(__name__)

class FacebookOAuthService:
    
    @staticmethod
    def verify_facebook_token(access_token):
        """Xác thực Facebook access token"""
        try:
            # Verify token với Facebook
            app_id = current_app.config['FACEBOOK_APP_ID']
            app_secret = current_app.config['FACEBOOK_APP_SECRET']
            
            # Debug token
            debug_url = 'https://graph.facebook.com/debug_token'
            debug_params = {
                'input_token': access_token,
                'access_token': f'{app_id}|{app_secret}'
            }
            
            debug_response = requests.get(debug_url, params=debug_params)
            
            if debug_response.status_code != 200:
                logger.error(f"Facebook token debug failed: {debug_response.text}")
                return None
            
            debug_data = debug_response.json()
            
            if not debug_data.get('data', {}).get('is_valid'):
                logger.error("Facebook token is not valid")
                return None
            
            # Get user info
            user_url = 'https://graph.facebook.com/me'
            user_params = {
                'fields': 'id,name,email,picture',
                'access_token': access_token
            }
            
            user_response = requests.get(user_url, params=user_params)
            
            if user_response.status_code != 200:
                logger.error(f"Failed to get Facebook user info: {user_response.text}")
                return None
            
            user_info = user_response.json()
            
            # Facebook có thể không trả email nếu user không cấp quyền
            if not user_info.get('email'):
                logger.error("Facebook user has no email")
                return None
            
            return user_info
            
        except Exception as e:
            logger.error(f"Error verifying Facebook token: {str(e)}")
            return None
    
    @staticmethod
    def get_or_create_user(user_info):
        """Tạo hoặc lấy user từ Facebook info"""
        email = user_info.get('email')
        facebook_id = user_info.get('id')
        
        if not email:
            return None
        
        # Tìm user theo email
        user = User.query.filter_by(email=email.lower()).first()
        
        if user:
            # User đã tồn tại, cập nhật thông tin OAuth nếu chưa có
            if not user.oauth_provider:
                user.oauth_provider = 'facebook'
                user.oauth_id = facebook_id
                user.is_verified = True
                
                # Lấy avatar từ Facebook
                if user_info.get('picture', {}).get('data', {}).get('url'):
                    user.avatar_url = user_info['picture']['data']['url']
                
                db.session.commit()
            
            return user
        
        # Tạo user mới
        avatar_url = None
        if user_info.get('picture', {}).get('data', {}).get('url'):
            avatar_url = user_info['picture']['data']['url']
        
        user = User(
            email=email.lower(),
            full_name=user_info.get('name'),
            oauth_provider='facebook',
            oauth_id=facebook_id,
            avatar_url=avatar_url,
            is_verified=True,
            is_active=True
        )
        
        db.session.add(user)
        db.session.commit()
        
        logger.info(f"New user created via Facebook OAuth: {email}")
        
        return user
