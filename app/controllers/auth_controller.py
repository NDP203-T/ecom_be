from app.services.auth_service import AuthService
from app.services.otp_service import OTPService
from app.services.email_service import EmailService
import logging

logger = logging.getLogger(__name__)

class AuthController:
    
    @staticmethod
    def register(data):
        """Đăng ký user mới và gửi OTP"""
        # Kiểm tra email đã tồn tại
        if AuthService.find_user_by_email(data['email']):
            return {'error': 'Email already exists'}, 400
        
        # Validate password
        if len(data['password']) < 6:
            return {'error': 'Password must be at least 6 characters'}, 400
        
        # Tạo user mới (chưa verify)
        user = AuthService.create_user(
            email=data['email'],
            password=data['password'],
            full_name=data.get('full_name')
        )
        
        # Tạo và gửi OTP
        otp_code = OTPService.create_otp(user.email)
        logger.info(f"OTP created for {user.email}: {otp_code}")
        print(f"🔑 OTP for {user.email}: {otp_code}")
        
        email_sent = EmailService.send_otp_email(user.email, otp_code)
        if not email_sent:
            logger.warning(f"Failed to send OTP email to {user.email}")
        
        return {
            'message': 'User registered successfully. Please check your email for OTP',
            'user': user.to_dict()
        }, 201
    
    @staticmethod
    def verify_otp(data):
        """Xác thực OTP"""
        email = data.get('email')
        code = data.get('code')
        
        if not OTPService.verify_otp(email, code):
            return {'error': 'Invalid or expired OTP'}, 400
        
        # Cập nhật user thành verified
        user = AuthService.find_user_by_email(email)
        if user:
            user.is_verified = True
            from app import db
            db.session.commit()
        
        return {'message': 'Email verified successfully'}, 200
    
    @staticmethod
    def resend_otp(data):
        """Gửi lại OTP"""
        email = data.get('email')
        
        # Kiểm tra user có tồn tại không
        user = AuthService.find_user_by_email(email)
        if not user:
            return {'error': 'Email not found'}, 404
        
        # Nếu đã verify rồi thì không cần gửi lại
        if user.is_verified:
            return {'error': 'Email already verified'}, 400
        
        # Tạo OTP mới và gửi
        otp_code = OTPService.create_otp(email)
        EmailService.send_otp_email(email, otp_code)
        
        return {'message': 'OTP sent successfully'}, 200
    
    @staticmethod
    def login(data):
        """Đăng nhập"""
        # Tìm user theo email
        user = AuthService.find_user_by_email(data['email'])
        
        # Kiểm tra user và password
        if not user or not AuthService.verify_password(user, data['password']):
            return {'error': 'Invalid email or password'}, 401
        
        # Kiểm tra email đã verify chưa
        if not user.is_verified:
            return {'error': 'Please verify your email first'}, 403
        
        # Tạo access token và refresh token
        access_token, refresh_token = AuthService.generate_tokens(user.id)
        
        return {
            'message': 'Login successful',
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': user.to_dict()
        }, 200

    @staticmethod
    def refresh_token(user_id):
        """Làm mới access token"""
        from flask_jwt_extended import create_access_token
        from datetime import timedelta
        
        access_token = create_access_token(
            identity=user_id,
            expires_delta=timedelta(hours=1)
        )
        
        return {'access_token': access_token}, 200
