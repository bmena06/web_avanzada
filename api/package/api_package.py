from flask import Blueprint, request
from models.package import PackageModel
from Config.db import db
from models.user import UserModel

# Crear un Blueprint para las rutas relacionadas con los paquetes
package_bp = Blueprint('package', __name__)

@package_bp.route('/newpackage', methods=['POST'])
def create_package():
    """
    Ruta para crear un nuevo paquete mediante una solicitud POST.

    Parámetros:
    - Se espera un cuerpo JSON con los datos del paquete a crear.

    Retorna:
    - Un mensaje de éxito y código de estado 201 si el paquete se crea exitosamente.

    Esta ruta permite crear un nuevo paquete utilizando los datos proporcionados en el cuerpo de la solicitud.
    El paquete se crea en la base de datos y se responde con un mensaje de éxito.
    """
    data = request.get_json()
    new_package = PackageModel(**data)
    new_package.save_to_db()
    return {"mensaje": "Paquete creado exitosamente"}, 201

@package_bp.route('/package/<int:id>', methods=['GET'])
def get_package(id):
    """
    Ruta para obtener los detalles de un paquete específico por su ID.

    Parámetros:
    - id: El ID del paquete que se desea recuperar.

    Retorna:
    - Los datos del paquete en formato JSON y código de estado 200 si se encuentra.
    - Un mensaje de error y código de estado 404 si el paquete no se encuentra.

    Esta ruta permite recuperar los detalles de un paquete específico proporcionando su ID.
    Si el paquete se encuentra en la base de datos, se retornan sus datos en formato JSON.
    Si el paquete no se encuentra, se devuelve un mensaje de error y se establece un código de estado 404.
    """
    package = PackageModel.query.get(id)
    if package:
        return package.json(), 200
    return {"mensaje": "Paquete no encontrado"}, 404

@package_bp.route('/updatepackage/<int:id>', methods=['PUT'])
def update_package(id):
    """
    Ruta para actualizar los detalles de un paquete específico por su ID mediante una solicitud PUT.

    Parámetros:
    - id: El ID del paquete que se desea actualizar.
    - Se espera un cuerpo JSON con los datos actualizados del paquete.

    Retorna:
    - Un mensaje de éxito y código de estado 200 si el paquete se actualiza exitosamente.
    - Un mensaje de error y código de estado 404 si el paquete no se encuentra.

    Esta ruta permite actualizar los detalles de un paquete específico proporcionando su ID y los datos actualizados en el cuerpo de la solicitud.
    Si el paquete se encuentra en la base de datos, se actualizan sus datos y se responde con un mensaje de éxito.
    Si el paquete no se encuentra, se devuelve un mensaje de error y se establece un código de estado 404.
    """
    package = PackageModel.query.get(id)
    if package:
        data = request.get_json()
        package.date = data['date']
        package.active = data['active']
        package.amount = data['amount']
        package.update_in_db()
        return {"mensaje": "Paquete actualizado exitosamente"}, 200
    return {"mensaje": "Paquete no encontrado"}, 404

@package_bp.route('/deletepackage/<int:id>', methods=['DELETE'])
def delete_package(id):
    """
    Ruta para eliminar un paquete específico por su ID mediante una solicitud DELETE.

    Parámetros:
    - id: El ID del paquete que se desea eliminar.

    Retorna:
    - Un mensaje de éxito y código de estado 200 si el paquete se elimina exitosamente.
    - Un mensaje de error y código de estado 404 si el paquete no se encuentra.

    Esta ruta permite eliminar un paquete específico proporcionando su ID.
    Si el paquete se encuentra en la base de datos, se elimina y se responde con un mensaje de éxito.
    Si el paquete no se encuentra, se devuelve un mensaje de error y se establece un código de estado 404.
    """
    package = PackageModel.query.get(id)
    if package:
        package.delete_from_db()
        return {"mensaje": "Paquete eliminado exitosamente"}, 200
    return {"mensaje": "Paquete no encontrado"}, 404

@package_bp.route('/packages', methods=['GET'])
def get_packages():
    """
    Ruta para obtener una lista de todos los paquetes.

    Retorna:
    - Una lista de todos los paquetes en formato JSON y código de estado 200.

    Esta ruta permite recuperar una lista de todos los paquetes disponibles en la base de datos.
    Los datos de los paquetes se devuelven en formato JSON como una lista.
    """
    packages = PackageModel.query.join(UserModel).add_columns(UserModel.name.label('user_name')).all()

    package_list = []
    for package, user_name in packages:
        package_data = package.json()
        package_data['user_name'] = user_name
        package_list.append(package_data)
    return {"packages": package_list}, 200
