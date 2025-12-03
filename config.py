"""
config settings for flask 
"""
import os
from pathlib import Path

# build paths
BASE_DIR = Path(__file__).resolve().parent
INSTANCE_DIR = BASE_DIR / 'instance'

class Config:
    """base config class"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # load database URI from instance config or environment variable
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://booktracker_user:booktracker_pass@localhost:5432/booktracker_db'

class DevelopmentConfig(Config):
    """development configuration."""
    DEBUG = True

class ProductionConfig(Config):
    """production configuration."""
    DEBUG = False

# configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
