from flask import Flask
import os
from config import config
from routes import main_bp

def create_app(config_name='development'):
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Create upload folder if it doesn't exist
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    
    # Register blueprints
    app.register_blueprint(main_bp)
    
    return app

# Create app instance for Gunicorn
app = create_app(os.environ.get('FLASK_ENV', 'production'))

if __name__ == '__main__':
    # Use production config if FLASK_ENV is not set
    config_name = os.environ.get('FLASK_ENV', 'production')
    app = create_app(config_name)
    port = int(os.environ.get('PORT', 5000))
    
    # Debug only in development
    debug = config_name == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)
