"""Flight Catalog Service Application"""
from flask import Flask


def create_app():
    """Application factory"""
    app = Flask(__name__)
    app.config['JSON_SORT_KEYS'] = False
    
    # Register blueprints
    from app.routes import flights_bp
    app.register_blueprint(flights_bp)
    
    return app
