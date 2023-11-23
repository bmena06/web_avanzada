from flask import Blueprint, jsonify, request
from models.rol import RolModel
from Config.db import db

# Crea un Blueprint para las rutas relacionadas con roles
rol_bp = Blueprint('rol', __name__)

@rol_bp.route('/newrol', methods=['POST'])
def create_rol():
    """
    Ruta para crear un nuevo rol mediante una solicitud POST.

    Parámetros:
    - Se espera un cuerpo JSON con los datos del nuevo rol.

    Retorna:
    - Un mensaje de éxito y código de estado 201 si el rol se crea exitosamente.

    Esta ruta permite crear un nuevo rol proporcionando los datos del rol en el cuerpo de la solicitud.
    Los datos del rol incluyen un nombre (name) y una compensación (compensation).
    Se responde con un mensaje de éxito y un código de estado 201 una vez que se crea el rol en la base de datos.
    """
    data = request.get_json()
    rol_name = data.get('name')

    # Verificar si ya existe un rol con el mismo nombre
    existing_rol = RolModel.query.filter_by(name=rol_name).first()
    if existing_rol:
        return jsonify({"mensaje": f"Ya existe un rol con el nombre '{rol_name}'"}), 400

    # Crear y guardar el nuevo rol
    new_rol = RolModel(**data)
    new_rol.save_to_db()
    
    return {"mensaje": "Rol creado exitosamente"}, 201


@rol_bp.route('/rol/<int:id>', methods=['GET'])
def get_rol(id):
    """
    Ruta para obtener los detalles de un rol específico por su ID.

    Parámetros:
    - id: El ID del rol que se desea recuperar.

    Retorna:
    - Los datos del rol en formato JSON y código de estado 200 si se encuentra.
    - Un mensaje de error y código de estado 404 si el rol no se encuentra.

    Esta ruta permite recuperar los detalles de un rol específico proporcionando su ID.
    Si el rol se encuentra en la base de datos, se retornan sus datos en formato JSON.
    Si el rol no se encuentra, se devuelve un mensaje de error y se establece un código de estado 404.
    """
    rol = RolModel.query.get(id)
    if rol:
        return rol.json(), 200
    return {"mensaje": "Rol no encontrado"}, 404

@rol_bp.route('/updaterol/<int:id>', methods=['PUT'])
def update_rol(id):
    """
    Ruta para actualizar los detalles de un rol específico por su ID mediante una solicitud PUT.

    Parámetros:
    - id: El ID del rol que se desea actualizar.
    - Se espera un cuerpo JSON con los datos actualizados del rol.

    Retorna:
    - Un mensaje de éxito y código de estado 200 si el rol se actualiza exitosamente.
    - Un mensaje de error y código de estado 404 si el rol no se encuentra.

    Esta ruta permite actualizar los detalles de un rol específico proporcionando su ID y los datos actualizados en el cuerpo de la solicitud.
    Si el rol se encuentra en la base de datos, se actualizan sus datos y se responde con un mensaje de éxito.
    Si el rol no se encuentra, se devuelve un mensaje de error y se establece un código de estado 404.
    """
    rol = RolModel.query.get(id)
    if rol:
        data = request.get_json()
        rol.name = data['name']
        rol.compensation = data['compensation']
        rol.update_in_db()
        return {"mensaje": "Rol actualizado exitosamente"}, 200
    return {"mensaje": "Rol no encontrado"}, 404

@rol_bp.route('/deleterol/<int:id>', methods=['DELETE'])
def delete_rol(id):
    """
    Ruta para eliminar un rol específico por su ID mediante una solicitud DELETE.

    Parámetros:
    - id: El ID del rol que se desea eliminar.

    Retorna:
    - Un mensaje de éxito y código de estado 200 si el rol se elimina exitosamente.
    - Un mensaje de error y código de estado 404 si el rol no se encuentra.

    Esta ruta permite eliminar un rol específico proporcionando su ID.
    Si el rol se encuentra en la base de datos, se elimina y se responde con un mensaje de éxito.
    Si el rol no se encuentra, se devuelve un mensaje de error y se establece un código de estado 404.
    """
    rol = RolModel.query.get(id)
    if rol:
        rol.delete_from_db()
        return {"mensaje": "Rol eliminado exitosamente"}, 200
    return {"mensaje": "Rol no encontrado"}, 404

@rol_bp.route('/rols', methods=['GET'])
def get_rols():
    """
    Ruta para obtener una lista de todos los roles.

    Retorna:
    - Una lista de todos los roles en formato JSON y código de estado 200.

    Esta ruta permite recuperar una lista de todos los roles disponibles en la base de datos.
    Los datos de los roles se devuelven en formato JSON como una lista.
    """
    rols = RolModel.query.all()
    return {"roles": [rol.json() for rol in rols]}, 200
