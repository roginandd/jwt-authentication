import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # ✅ Correct MySQL connection string format
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@"
        f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )

    # ✅ Disable SQLAlchemy event system overhead
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ⚠️ Fixed typo: "UPLOAD_FOLER" → "UPLOAD_FOLDER"
    # Also set a fallback path (e.g., "uploads")
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')

    # ✅ Set default logging directory
    LOG_FOLDER = os.getenv('LOG_FOLDER', 'logs')

    # ✅ Enable debug mode if specified, otherwise False
    DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() in ('true', '1', 'yes')
    
    
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')