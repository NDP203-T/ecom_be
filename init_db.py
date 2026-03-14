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
        from app.models import User
        print("✅ Models loaded successfully!")

if __name__ == '__main__':
    init_database()
