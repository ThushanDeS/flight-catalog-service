"""
Flight Catalog Service - Main Application Entry Point
Student A: Flight Catalog Microservice
"""

import os
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from datetime import datetime

# Import from app package
from app.routes import flights_bp
import importlib

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
CORS(app)

# Keep default JSON encoder (custom encoder removed to avoid import errors)

# Register blueprints
app.register_blueprint(flights_bp)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for container orchestration"""
    try:
        models = importlib.import_module('app.models')
        db_status = getattr(models, 'get_db_status', lambda: {"connected": False})()
    except Exception:
        db_status = {"connected": False}

    return jsonify({
        "service": "flight-catalog",
        "status": "healthy" if db_status["connected"] else "degraded",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat(),
        "database": db_status
    })

@app.route('/', methods=['GET'])
def root():
    """Root endpoint with API information"""
    return jsonify({
        "name": "Flight Catalog Service",
        "description": "Microservice for managing flight information",
        "version": "1.0.0",
        "endpoints": {
            "GET /health": "Health check",
            "GET /api/flights": "List all flights (with optional filters)",
            "GET /api/flights/{id}": "Get flight by ID",
            "POST /api/flights": "Create new flight",
            "PATCH /api/flights/{id}/seats": "Update available seats",
            "GET /api/flights/search": "Search flights by origin/destination"
        },
        "documentation": "/swagger.yaml"
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5001))
    debug = os.getenv('FLASK_ENV') == 'development'
    
    print("=" * 50)
    print("🚀 Flight Catalog Service Starting...")
    print("=" * 50)
    print(f"📡 Port: {port}")
    print(f"🔧 Debug mode: {'ON' if debug else 'OFF'}")
    print(f"🌐 Environment: {os.getenv('FLASK_ENV', 'production')}")
    print("=" * 50)
    
    # Initialize database with sample data (import at runtime to avoid import-time issues)
    with app.app_context():
        try:
            models = importlib.import_module('app.models')
            init_db = getattr(models, 'init_db', None)
            if callable(init_db):
                init_db()
        except Exception:
            pass
    
    app.run(host='0.0.0.0', port=port, debug=debug)