from flask import Blueprint, request
from models.product import ProductModel
from Config.db import db

product_bp = Blueprint('product', __name__)

@product_bp.route('/newproduct', methods=['POST'])
def create_product():
    data = request.get_json()
    new_product = ProductModel(**data)
    new_product.save_to_db()
    return {"mensaje": "Producto creado exitosamente"}, 201

@product_bp.route('/product/<int:id>', methods=['GET'])
def get_product(id):
    product = ProductModel.query.get(id)
    if product:
        return product.json(), 200
    return {"mensaje": "Producto no encontrado"}, 404

@product_bp.route('/updateproduct/<int:id>', methods=['PUT'])
def update_product(id):
    product = ProductModel.query.get(id)
    if product:
        data = request.get_json()
        product.name = data['nombre']
        product.compensation = data['compensation']
        product.update_in_db()
        return {"mensaje": "Producto actualizado exitosamente"}, 200
    return {"mensaje": "Producto no encontrado"}, 404

@product_bp.route('/deleteproduct/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = ProductModel.query.get(id)
    if product:
        product.delete_from_db()
        return {"mensaje": "Producto eliminado exitosamente"}, 200
    return {"mensaje": "Producto no encontrado"}, 404

@product_bp.route('/products', methods=['GET'])
def get_products():
    products = ProductModel.query.all()
    return {"Producto": [rol.json() for rol in products]}, 200
