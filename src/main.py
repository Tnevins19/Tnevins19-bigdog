import os
import sys

# Add the parent directory of src to the Python path if not already there
# This is crucial for running src.main as a module from the project root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from flask import Flask, send_from_directory
from flask_cors import CORS

# Initialize db here, but don't import models yet to avoid circular imports
from src.models import db

def create_app():
    app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
    CORS(app) # Enable CORS for all routes
    app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

    # Database configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    with app.app_context():
        # Import models and blueprints inside app context to avoid circular imports
        from src.models.user import User # Assuming User model exists
        from src.models.product import Product
        from src.models.category import Category
        from src.routes.user import user_bp
        from src.routes.products import products_bp

        db.create_all()

        app.register_blueprint(user_bp, url_prefix='/api')
        app.register_blueprint(products_bp, url_prefix='/api')

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve(path):
        static_folder_path = app.static_folder
        if static_folder_path is None:
                return "Static folder not configured", 404

        if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
            return send_from_directory(static_folder_path, path)
        else:
            index_path = os.path.join(static_folder_path, 'index.html')
            if os.path.exists(index_path):
                return send_from_directory(static_folder_path, 'index.html')
            else:
                return "index.html not found", 404
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)


