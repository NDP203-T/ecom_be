import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key')
    
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://ecom_user:ecom_pass@localhost:5432/ecom_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    
    CLOUDINARY_CLOUD_NAME = os.getenv('CLOUDINARY_CLOUD_NAME')
    CLOUDINARY_API_KEY = os.getenv('CLOUDINARY_API_KEY')
    CLOUDINARY_API_SECRET = os.getenv('CLOUDINARY_API_SECRET')
