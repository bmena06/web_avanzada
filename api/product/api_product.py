from flask import Blueprint, request
from models.product import ProductModel
from Config.db import db

# Crea un Blueprint para las rutas relacionadas con productos
product_bp = Blueprint('product', __name__)

@product_bp.route('/newproduct', methods=['POST'])
def create_product():
    """
    Ruta para crear un nuevo producto mediante una solicitud POST.

    Parámetros:
    - Se espera un cuerpo JSON con los datos del nuevo producto, incluyendo 'name' y 'price'.

    Retorna:
    - Un mensaje de éxito y código de estado 201 si el producto se crea exitosamente.

    Esta ruta permite crear un nuevo producto proporcionando los datos necesarios en el cuerpo de la solicitud.
    El producto se crea en la base de datos y se responde con un mensaje de éxito y un código de estado 201.
    """
    data = request.get_json()
    new_product = ProductModel(**data)
    new_product.save_to_db()
    return {"mensaje": "Producto creado exitosamente"}, 201

@product_bp.route('/product/<int:id>', methods=['GET'])
def get_product(id):
    """
    Ruta para obtener los detalles de un producto específico por su ID.

    Parámetros:
    - id: El ID del producto que se desea recuperar.

    Retorna:
    - Los datos del producto en formato JSON y código de estado 200 si se encuentra.
    - Un mensaje de error y código de estado 404 si el producto no se encuentra.

    Esta ruta permite recuperar los detalles de un producto específico proporcionando su ID.
    Si el producto se encuentra en la base de datos, se retornan sus datos en formato JSON.
    Si el producto no se encuentra, se devuelve un mensaje de error y se establece un código de estado 404.
    """
    product = ProductModel.query.get(id)
    if product:
        return product.json(), 200
    return {"mensaje": "Producto no encontrado"}, 404

@product_bp.route('/updateproduct/<int:id>', methods=['PUT'])
def update_product(id):
    """
    Ruta para actualizar los detalles de un producto específico por su ID mediante una solicitud PUT.

    Parámetros:
    - id: El ID del producto que se desea actualizar.
    - Se espera un cuerpo JSON con los datos actualizados del producto.

    Retorna:
    - Un mensaje de éxito y código de estado 200 si el producto se actualiza exitosamente.
    - Un mensaje de error y código de estado 404 si el producto no se encuentra.

    Esta ruta permite actualizar los detalles de un producto específico proporcionando su ID y los datos actualizados en el cuerpo de la solicitud.
    Si el producto se encuentra en la base de datos, se actualizan sus datos y se responde con un mensaje de éxito.
    Si el producto no se encuentra, se devuelve un mensaje de error y se establece un código de estado 404.
    """
    product = ProductModel.query.get(id)
    if product:
        data = request.get_json()
        product.name = data['name']
        product.price = data['price']
        product.update_in_db()
        return {"mensaje": "Producto actualizado exitosamente"}, 200
    return {"mensaje": "Producto no encontrado"}, 404

@product_bp.route('/deleteproduct/<int:id>', methods=['DELETE'])
def delete_product(id):
    """
    Ruta para eliminar un producto específico por su ID mediante una solicitud DELETE.

    Parámetros:
    - id: El ID del producto que se desea eliminar.

    Retorna:
    - Un mensaje de éxito y código de estado 200 si el producto se elimina exitosamente.
    - Un mensaje de error y código de estado 404 si el producto no se encuentra.

    Esta ruta permite eliminar un producto específico proporcionando su ID.
    Si el producto se encuentra en la base de datos, se elimina y se responde con un mensaje de éxito.
    Si el producto no se encuentra, se devuelve un mensaje de error y se establece un código de estado 404.
    """
    product = ProductModel.query.get(id)
    if product:
        product.delete_from_db()
        return {"mensaje": "Producto eliminado exitosamente"}, 200
    return {"mensaje": "Producto no encontrado"}, 404

@product_bp.route('/products', methods=['GET'])
def get_products():
    """
    Ruta para obtener una lista de todos los productos.

    Retorna:
    - Una lista de todos los productos en formato JSON y código de estado 200.

    Esta ruta permite recuperar una lista de todos los productos disponibles en la base de datos.
    Los datos de los productos se devuelven en formato JSON como una lista.
    """
    products = ProductModel.query.all()
    return {"productos": [producto.json() for producto in products]}, 200
