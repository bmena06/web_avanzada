from flask import Blueprint, request
from models.rol import RolModel
from models.user import UserModel
from Config.db import db

# Crea un Blueprint para las rutas relacionadas con usuarios
user_bp = Blueprint('user', __name__)
@user_bp.route('/newuser', methods=['POST'])
def create_user():
    data = request.get_json()
    rol_name = data.get('rol_name')

    rol_id = get_rol_id_by_name(rol_name)

    # Verifica si se encontró el rol
    if rol_id is not None:
        # Asigna el ID del rol al usuario
        data['id_rol'] = rol_id
        del data['rol_name']  # Elimina el nombre del rol del diccionario

        # Crea y guarda el nuevo usuario
        new_user = UserModel(**data)
        new_user.save_to_db()
        return {"mensaje": "Usuario creado exitosamente"}, 201
    else:
        return {"mensaje": f"No se encontró un rol con el nombre '{rol_name}'"}, 404


def get_rol_id_by_name(rol_name):
    rol = RolModel.query.filter_by(name=rol_name).first()
    if rol:
        return rol.id
    else:
        return None

    

@user_bp.route('/user/<int:id>', methods=['GET'])
def get_user(id):
    """
    Ruta para obtener los detalles de un usuario específico por su ID.

    Parámetros:
    - id: El ID del usuario que se desea recuperar.

    Retorna:
    - Los datos del usuario en formato JSON y código de estado 200 si se encuentra.
    - Un mensaje de error y código de estado 404 si el usuario no se encuentra.

    Esta ruta permite recuperar los detalles de un usuario específico proporcionando su ID.
    Si el usuario se encuentra en la base de datos, se retornan sus datos en formato JSON.
    Si el usuario no se encuentra, se devuelve un mensaje de error y se establece un código de estado 404.
    """
    user = UserModel.query.get(id)
    if user:
        return user.json(), 200
    return {"mensaje": "Usuario no encontrado"}, 404

@user_bp.route('/updateuser/<int:id>', methods=['PUT'])
def update_user(id):
    """
    Ruta para actualizar los detalles de un usuario específico por su ID mediante una solicitud PUT.

    Parámetros:
    - id: El ID del usuario que se desea actualizar.
    - Se espera un cuerpo JSON con los datos actualizados del usuario.

    Retorna:
    - Un mensaje de éxito y código de estado 200 si el usuario se actualiza exitosamente.
    - Un mensaje de error y código de estado 404 si el usuario no se encuentra.

    Esta ruta permite actualizar los detalles de un usuario específico proporcionando su ID y los datos actualizados en el cuerpo de la solicitud.
    Si el usuario se encuentra en la base de datos, se actualizan sus datos y se responde con un mensaje de éxito.
    Si el usuario no se encuentra, se devuelve un mensaje de error y se establece un código de estado 404.
    """
    user = UserModel.query.get(id)
    if user:
        data = request.get_json()
        user.name = data['name']
        user.email = data['email']
        user.password = data['password']
        user.id_rol = data['id_rol']
        user.update_in_db()
        return {"mensaje": "Usuario actualizado exitosamente"}, 200
    return {"mensaje": "Usuario no encontrado"}, 404

@user_bp.route('/deleteuser/<int:id>', methods=['DELETE'])
def delete_user(id):
    """
    Ruta para eliminar un usuario específico por su ID mediante una solicitud DELETE.

    Parámetros:
    - id: El ID del usuario que se desea eliminar.

    Retorna:
    - Un mensaje de éxito y código de estado 200 si el usuario se elimina exitosamente.
    - Un mensaje de error y código de estado 404 si el usuario no se encuentra.

    Esta ruta permite eliminar un usuario específico proporcionando su ID.
    Si el usuario se encuentra en la base de datos, se elimina y se responde con un mensaje de éxito.
    Si el usuario no se encuentra, se devuelve un mensaje de error y se establece un código de estado 404.
    """
    user = UserModel.query.get(id)
    if user:
        user.delete_from_db()
        return {"mensaje": "Usuario eliminado exitosamente"}, 200
    return {"mensaje": "Usuario no encontrado"}, 404

@user_bp.route('/users', methods=['GET'])
def get_users():
    """
    Ruta para obtener una lista de todos los usuarios con detalles de rol.

    Retorna:
    - Una lista de todos los usuarios con detalles de rol en formato JSON y código de estado 200.

    Esta ruta permite recuperar una lista de todos los usuarios disponibles en la base de datos con detalles de rol.
    Los datos de los usuarios se devuelven en formato JSON como una lista, incluyendo el nombre del rol.
    """
    users = UserModel.query.join(RolModel).add_columns(RolModel.name.label('rol_name')).all()

    user_list = []
    for user, rol_name in users:
        user_data = user.json()
        user_data['rol_name'] = rol_name
        user_list.append(user_data)

    return {"usuarios": user_list}, 200

