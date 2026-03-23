from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_mail import Mail
from flask_swagger_ui import get_swaggerui_blueprint
import cloudinary
from config import Config

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    CORS(app)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    mail.init_app(app)
    
    cloudinary.config(
        cloud_name=app.config['CLOUDINARY_CLOUD_NAME'],
        api_key=app.config['CLOUDINARY_API_KEY'],
        api_secret=app.config['CLOUDINARY_API_SECRET']
    )
    
    # Swagger UI
    SWAGGER_URL = '/api/docs'
    API_URL = '/static/swagger.json'
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "E-Commerce API"
        }
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
    
    # Routes
    from app.routes import auth, decrypt, dashboard, user, product, category
    app.register_blueprint(auth.bp)
    app.register_blueprint(decrypt.bp)
    app.register_blueprint(dashboard.bp)
    app.register_blueprint(user.bp)
    app.register_blueprint(product.bp)
    app.register_blueprint(category.bp)
    
    # Serve swagger.json
    @app.route('/static/swagger.json')
    def swagger_json():
        from flask import send_file
        import os
        swagger_path = os.path.join(app.root_path, 'swagger', 'swagger.json')
        return send_file(swagger_path)
    
    # Decrypt helper page
    @app.route('/decrypt')
    def decrypt_page():
        from flask import render_template
        return render_template('decrypt.html')
    
    return app
