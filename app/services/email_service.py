from flask_mail import Message
from app import mail
import logging

logger = logging.getLogger(__name__)

class EmailService:
    
    @staticmethod
    def send_otp_email(email, otp_code):
        """Gửi OTP qua email"""
        try:
            logger.info(f"Attempting to send OTP to {email}")
            
            msg = Message(
                subject='Xác thực tài khoản - E-Commerce',
                recipients=[email]
            )
            
            msg.html = f"""
            <html>
                <body style="font-family: Arial, sans-serif;">
                    <h2>Xác thực tài khoản</h2>
                    <p>Mã OTP của bạn là:</p>
                    <h1 style="color: #4CAF50; font-size: 32px; letter-spacing: 5px;">{otp_code}</h1>
                    <p>Mã này sẽ hết hạn sau 10 phút.</p>
                    <p>Nếu bạn không yêu cầu mã này, vui lòng bỏ qua email này.</p>
                </body>
            </html>
            """
            
            mail.send(msg)
            logger.info(f"OTP sent successfully to {email}")
            return True
        except Exception as e:
            logger.error(f"Error sending email to {email}: {str(e)}")
            print(f"❌ Error sending email: {str(e)}")
            return False
