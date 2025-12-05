"""
Application Factory Pattern:
- Separates app creation from configuration
- Enables multiple app instances (testing, production)
- Avoids circular imports
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Initialize extensions (but don't bind to app yet)
db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class='config.Config'):
    """
    Application factory function.
    Creates and configures Flask application instance.
    """
    # Create Flask app
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config_class)
    
    # Initialize extensions with app
    # init_app: binds extension to this specific app instance
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Register blueprints (route collections)
    from app.routes import main_bp
    app.register_blueprint(main_bp)
    
    return app
