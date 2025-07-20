import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from main import create_app, db
from models.product import Product
from models.category import Category
from models.user import User # Assuming User model exists

app = create_app()

with app.app_context():
    db.create_all()


