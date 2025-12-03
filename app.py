"""
Flask Book Tracker Application
Main application file with application factory pattern.
"""
from flask import Flask
from config import config
from models.book import db
from routes.book_routes import book_bp
import os

def create_app(config_name='development'):
    """
    Application factory function.
    
    Args:
        config_name: Configuration name (development/production)
    
    Returns:
        Flask application instance
    """
    # Create Flask app
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Try to load instance config if it exists
    try:
        app.config.from_pyfile('instance/config.py')
    except:
        pass
    
    # Initialize database
    db.init_app(app)
    
    # Register blueprints
    app.register_blueprint(book_bp)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app

# Create application instance
app = create_app()

if __name__ == '__main__':
    """
    Run the application in development mode.
    For production, use a WSGI server like Gunicorn.
    """
    app.run(debug=True, host='0.0.0.0', port=5000)
