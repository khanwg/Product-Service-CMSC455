# CMSC 455
# Wahaaj Khan
# Assignment 2
from flask import Flask, jsonify
from flask_httpauth import HTTPDigestAuth
from flask_sqlalchemy import SQLAlchemy
from flask import request
import os

from sqlalchemy import true

basedir = os.path.abspath(os.path.dirname(__file__))
# App configuration
app = Flask(__name__)
app.config['SECRET_KEY'] = 'UNguessable'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'products.sqlite')
db = SQLAlchemy(app)
auth = HTTPDigestAuth()
USERS = {
    "khanwg": "P@ssword!"
}


# Product Model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)


# Endpoint 1 : Retrieves full list of Products
@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    product_list = [{"id": product.id, "name": product.name, "price": product.price, "quantity": product.quantity} for
                    product in products]
    return jsonify({"product": product_list})


# Endpoint 2: Get a specific product by ID
@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get(product_id)
    if product:
        return jsonify(
            {"product": {"id": product.id, "name": product.name, "price": product.price, "quantity": product.quantity}})
    else:
        return jsonify({"error": "Product not found"}), 404


# Endpoint 3: Create a new product
@app.route('/products', methods=['POST'])
@auth.login_required
def add_product():
    data = request.get_json()

    required_keywords = ["id", "name", "price", "quantity"]
    if not all(key in data for key in required_keywords):
        return jsonify({"error": "missing required info"}), 400

    new_product = Product(id=data['id'], name=data['name'], price=data['price'], quantity=data['quantity'])
    db.session.add(new_product)
    db.session.commit()

    return jsonify({"message": "Product created",
                    "product": {"id": new_product.id, "name": new_product.name, "price": new_product.price,
                                "quantity": new_product.quantity}}), 201


@auth.get_password
def get_pw(username):
    if username in USERS:
        return USERS.get(username)
    return None


if __name__ == '__main__':
    # with app.app_context():
    # db.create_all()
    app.run(debug=true)
