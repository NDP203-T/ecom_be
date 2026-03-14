from datetime import datetime, timedelta
from app import db
from app.models.user import OTP
import random
import string

class OTPService:
    
    @staticmethod
    def generate_otp_code():
        """Tạo mã OTP 6 số"""
        return ''.join(random.choices(string.digits, k=6))
    
    @staticmethod
    def create_otp(email):
        """Tạo OTP mới cho email"""
        code = OTPService.generate_otp_code()
        expires_at = datetime.utcnow() + timedelta(minutes=10)
        
        otp = OTP(
            email=email,
            code=code,
            expires_at=expires_at
        )
        
        db.session.add(otp)
        db.session.commit()
        
        return code
    
    @staticmethod
    def verify_otp(email, code):
        """Xác thực OTP"""
        otp = OTP.query.filter_by(
            email=email,
            code=code,
            is_used=False
        ).first()
        
        if not otp:
            return False
        
        if datetime.utcnow() > otp.expires_at:
            return False
        
        otp.is_used = True
        db.session.commit()
        
        return True
