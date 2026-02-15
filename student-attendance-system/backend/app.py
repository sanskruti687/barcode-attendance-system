"""
Main Flask application for Student Attendance System
"""
from flask import Flask, send_file
from flask_cors import CORS
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.config import Config
from routes import api

# Initialize Flask app
app = Flask(__name__)

# Load configuration
app.config.from_object(Config)

# Enable CORS
CORS(app)

# Register blueprints
app.register_blueprint(api)


# ==================== MAIN ROUTES ====================

@app.route('/')
def index():
    """Serve the main dashboard page"""
    frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend', 'index.html')
    return send_file(frontend_path)


@app.route('/admin')
def admin():
    """Serve the admin panel page"""
    frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend', 'admin.html')
    return send_file(frontend_path)


# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    from flask import jsonify
    return jsonify({
        'success': False,
        'message': 'Resource not found'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    from flask import jsonify
    return jsonify({
        'success': False,
        'message': 'Internal server error'
    }), 500


# ==================== MAIN ====================

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🎓 Student Attendance System with Barcode Scanner")
    print("="*60)
    print(f"✓ Server running on: http://{Config.HOST}:{Config.PORT}")
    print(f"✓ Dashboard: http://localhost:{Config.PORT}/")
    print(f"✓ Admin Panel: http://localhost:{Config.PORT}/admin")
    print(f"✓ Debug mode: {Config.DEBUG}")
    print("="*60 + "\n")
    
    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG
    )