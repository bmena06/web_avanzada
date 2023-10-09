from flask import Blueprint, request
from Models.producto import ProductoModel
from Config.db import db

producto_bp = Blueprint('producto', __name__)

@producto_bp.route('/productos', methods=['POST'])
def crear_producto():
    data = request.get_json()
    nuevo_producto = ProductoModel(**data)
    nuevo_producto.save_to_db()
    return {"mensaje": "Producto creado exitosamente"}, 201

@producto_bp.route('/productos/<int:id>', methods=['GET'])
def obtener_producto(id):
    producto = ProductoModel.query.get(id)
    if producto:
        return producto.json(), 200
    return {"mensaje": "Producto no encontrado"}, 404

@producto_bp.route('/productos/<int:id>', methods=['PUT'])
def actualizar_producto(id):
    producto = ProductoModel.query.get(id)
    if producto:
        data = request.get_json()
        producto.nombre = data['nombre']
        producto.numero = data['numero']
        producto.update_in_db()
        return {"mensaje": "Producto actualizado exitosamente"}, 200
    return {"mensaje": "Producto no encontrado"}, 404

@producto_bp.route('/productos/<int:id>', methods=['DELETE'])
def eliminar_producto(id):
    producto = ProductoModel.query.get(id)
    if producto:
        producto.delete_from_db()
        return {"mensaje": "Producto eliminado exitosamente"}, 200
    return {"mensaje": "Producto no encontrado"}, 404

@producto_bp.route('/productos', methods=['GET'])
def obtener_todos_los_productos():
    productos = ProductoModel.query.all()
    return {"productos": [producto.json() for producto in productos]}, 200
