import os
from dotenv import load_dotenv

load_dotenv()

def _normalize_database_url(url: str | None) -> str | None:
    """
    Render/Heroku-style URLs sometimes use 'postgres://' which SQLAlchemy doesn't recognize.
    Normalize to 'postgresql://'.
    """
    if not url:
        return None
    if url.startswith("postgres://"):
        return "postgresql://" + url[len("postgres://") :]
    return url


class Config:
    """Flask configuration."""
    
    # Secret key for sessions
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = _normalize_database_url(
        os.environ.get("SQLALCHEMY_DATABASE_URI")
        or os.environ.get("DATABASE_URL")
    )
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }
    
    # Flask-Admin configuration
    FLASK_ADMIN_SWATCH = 'cerulean'  # Bootstrap theme
