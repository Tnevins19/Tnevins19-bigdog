from flask import Blueprint, request, jsonify
from src.models import db
from src.models.product import Product
from src.models.category import Category

products_bp = Blueprint("products", __name__)

@products_bp.route("/products", methods=["POST"])
def add_product():
    data = request.get_json()
    new_product = Product(
        name=data["name"],
        description=data.get("description"),
        price=data["price"],
        category_id=data["category_id"],
        download_url=data["download_url"]
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify({"message": "Product added successfully"}), 201

@products_bp.route("/products", methods=["GET"])
def get_products():
    products = Product.query.all()
    output = []
    for product in products:
        output.append({
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "category_id": product.category_id,
            "download_url": product.download_url
        })
    return jsonify({"products": output})

@products_bp.route("/categories", methods=["POST"])
def add_category():
    data = request.get_json()
    new_category = Category(
        name=data["name"]
    )
    db.session.add(new_category)
    db.session.commit()
    return jsonify({"message": "Category added successfully"}), 201

@products_bp.route("/categories", methods=["GET"])
def get_categories():
    categories = Category.query.all()
    output = []
    for category in categories:
        output.append({
            "id": category.id,
            "name": category.name
        })
    return jsonify({"categories": output})


