"""
Script để khởi tạo database và chạy migrations
"""
from app import create_app, db
from flask_migrate import init, migrate, upgrade
import os

def init_database():
    app = create_app()
    
    with app.app_context():
        # Tạo tất cả tables
        db.create_all()
        print("✅ Database tables created successfully!")
        
        # Import models để đảm bảo được load
        from app.models import User, OTP, Product, Order, OrderItem
        print("✅ Models loaded successfully!")
        
        # Tạo admin mặc định
        admin_email = os.getenv('ADMIN_EMAIL', 'admin@ecommerce.com')
        admin_password = os.getenv('ADMIN_PASSWORD', 'Admin@123456')
        
        existing_admin = User.query.filter_by(email=admin_email).first()
        
        if not existing_admin:
            admin = User(
                email=admin_email,
                full_name='System Admin',
                role='admin',
                is_verified=True
            )
            admin.set_password(admin_password)
            
            db.session.add(admin)
            db.session.commit()
            
            print(f"✅ Admin account created!")
            print(f"   Email: {admin_email}")
            print(f"   Password: {admin_password}")
            print(f"   ⚠️  CHANGE PASSWORD AFTER FIRST LOGIN!")
        else:
            print(f"ℹ️  Admin account already exists: {admin_email}")

if __name__ == '__main__':
    init_database()
