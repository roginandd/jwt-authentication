import os
import logging
from flask import Flask
from config import Config
from extensions import db  # ✅ import shared db instance
from flask_jwt_extended import JWTManager  # ✅ import JWT manager

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    jwt = JWTManager(app)  # ✅ initialize JWT with app

    # Configure logging
    os.makedirs(app.config['LOG_FOLDER'], exist_ok=True)
    logging.basicConfig(
        filename=f"{app.config['LOG_FOLDER']}/app.log",
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s'
    )

    # Import and register blueprints
    from controllers.auth_controller import auth_bp  # ✅ login & JWT routes
    from controllers.file_controller import file_bp  # ✅ your file endpoints

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(file_bp, url_prefix="/files")

    # Create tables (only for demo — in prod, use migrations)
    with app.app_context():
        db.create_all()

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
