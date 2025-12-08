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

if __name__ == '__main__':
    app = create_app('development')
    app.run(debug=True)
