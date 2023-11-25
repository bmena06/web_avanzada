from flask import Blueprint, request
from models.product import ProductModel
from models.production import ProductionModel
from Config.db import db
from models.product_logic import create_production_and_package
from models.user import UserModel

# Crea un Blueprint para las rutas relacionadas con producción
production_bp = Blueprint('production', __name__)

@production_bp.route('/newproduction', methods=['POST'])
def create_production():
    """
    Ruta para crear una nueva producción y paquete mediante una solicitud POST.

    Parámetros:
    - Se espera un cuerpo JSON con los datos de usuario (user_id) y producto (product_name).

    Retorna:
    - Un mensaje de éxito y código de estado 201 si la producción y el paquete se crean exitosamente.

    Esta ruta permite crear una nueva producción y paquete proporcionando los datos de usuario y producto en el cuerpo de la solicitud.
    La función create_production_and_package se encarga de crear la producción y el paquete necesarios en la base de datos.
    Se responde con un mensaje de éxito y un código de estado 201 una vez que se completan las operaciones.
    """
    data = request.get_json()
    user_id = data.get('user_id')
    product_name = data.get('product_id')

    # Busca el ID del producto por nombre
    product_id = get_product_id_by_name(product_name)

    # Verifica si se encontró el producto
    if product_id is not None:
        # Si se encontró el producto, crea la producción y el paquete
        create_production_and_package(user_id, product_id)
        return {"mensaje": "Producción creada exitosamente"}, 201
    else:
        # Si no se encontró el producto, responde con un mensaje de error
        return {"mensaje": f"No se encontró un producto con el nombre '{product_name}'"}, 404


def get_product_id_by_name(product_name):

    product = ProductModel.query.filter_by(name=product_name).first()

    if product:
        return product.id
    else:
        return None

@production_bp.route('/production/<int:id>', methods=['GET'])
def get_production(id):
    """
    Ruta para obtener los detalles de una producción específica por su ID.

    Parámetros:
    - id: El ID de la producción que se desea recuperar.

    Retorna:
    - Los datos de la producción en formato JSON y código de estado 200 si se encuentra.
    - Un mensaje de error y código de estado 404 si la producción no se encuentra.

    Esta ruta permite recuperar los detalles de una producción específica proporcionando su ID.
    Si la producción se encuentra en la base de datos, se retornan sus datos en formato JSON.
    Si la producción no se encuentra, se devuelve un mensaje de error y se establece un código de estado 404.
    """
    production = ProductionModel.query.get(id)
    if production:
        return production.json(), 200
    return {"mensaje": "Producción no encontrada"}, 404

@production_bp.route('/updateproduction/<int:id>', methods=['PUT'])
def update_production(id):
    """
    Ruta para actualizar los detalles de una producción específica por su ID mediante una solicitud PUT.

    Parámetros:
    - id: El ID de la producción que se desea actualizar.
    - Se espera un cuerpo JSON con los datos actualizados de la producción.

    Retorna:
    - Un mensaje de éxito y código de estado 200 si la producción se actualiza exitosamente.
    - Un mensaje de error y código de estado 404 si la producción no se encuentra.

    Esta ruta permite actualizar los detalles de una producción específica proporcionando su ID y los datos actualizados en el cuerpo de la solicitud.
    Si la producción se encuentra en la base de datos, se actualizan sus datos y se responde con un mensaje de éxito.
    Si la producción no se encuentra, se devuelve un mensaje de error y se establece un código de estado 404.
    """
    production = ProductionModel.query.get(id)
    if production:
        data = request.get_json()
        production.date = data['date']
        production.user_id = data['user_id']
        production.product_id = data['product_id']
        production.package_id = data['package_id']
        production.update_in_db()
        return {"mensaje": "Producción actualizada exitosamente"}, 200
    return {"mensaje": "Producción no encontrada"}, 404

@production_bp.route('/deleteproduction/<int:id>', methods=['DELETE'])
def delete_production(id):
    """
    Ruta para eliminar una producción específica por su ID mediante una solicitud DELETE.

    Parámetros:
    - id: El ID de la producción que se desea eliminar.

    Retorna:
    - Un mensaje de éxito y código de estado 200 si la producción se elimina exitosamente.
    - Un mensaje de error y código de estado 404 si la producción no se encuentra.

    Esta ruta permite eliminar una producción específica proporcionando su ID.
    Si la producción se encuentra en la base de datos, se elimina y se responde con un mensaje de éxito.
    Si la producción no se encuentra, se devuelve un mensaje de error y se establece un código de estado 404.
    """
    production = ProductionModel.query.get(id)
    if production:
        production.delete_from_db()
        return {"mensaje": "Producción eliminada exitosamente"}, 200
    return {"mensaje": "Producción no encontrada"}, 404

@production_bp.route('/productions', methods=['GET'])
def get_productions():
    
    user_id = request.args.get('user_id')
    if user_id!= '1':
        # Si se proporciona un user_id, obtenemos las producciones para ese usuario
        productions = ProductionModel.query.filter_by(user_id=user_id).join(UserModel).join(ProductModel).add_columns(UserModel.name.label('user_name'), ProductModel.name.label('product_name')).all()
    else:
        # Si no se proporciona un user_id, obtenemos todas las producciones
        print(user_id)
        productions = ProductionModel.query.join(UserModel).join(ProductModel).add_columns(UserModel.name.label('user_name'), ProductModel.name.label('product_name')).all()


    production_list = []
    for production, user_name, product_name in productions:
        production_data = production.json()
        production_data['user_name'] = user_name
        production_data['product_name'] = product_name
        production_list.append(production_data)

    return {"producciones": production_list}, 200

