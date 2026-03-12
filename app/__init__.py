from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import redis
import cloudinary
from config import Config

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
redis_client = None

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    CORS(app)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    
    global redis_client
    redis_client = redis.from_url(app.config['REDIS_URL'])
    
    cloudinary.config(
        cloud_name=app.config['CLOUDINARY_CLOUD_NAME'],
        api_key=app.config['CLOUDINARY_API_KEY'],
        api_secret=app.config['CLOUDINARY_API_SECRET']
    )
    
    from app.routes import auth, products, cart, orders
    app.register_blueprint(auth.bp)
    app.register_blueprint(products.bp)
    app.register_blueprint(cart.bp)
    app.register_blueprint(orders.bp)
    
    return app
