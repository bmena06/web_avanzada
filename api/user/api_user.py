from flask import Blueprint, request
from models.user import UserModel
from Config.db import db
from werkzeug.security import generate_password_hash, check_password_hash

user_bp = Blueprint('user', __name__)

@user_bp.route('/newuser', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = UserModel(**data)
    new_user.save_to_db()
    return {"mensaje": "Usuario creado exitosamente"}, 201

@user_bp.route('/user/<int:id>', methods=['GET'])
def get_user(id):
    user = UserModel.query.get(id)
    if user:
        return user.json(), 200
    return {"mensaje": "Usuario no encontrado"}, 404

@user_bp.route('/updateuser/<int:id>', methods=['PUT'])
def update_user(id):
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
    user = UserModel.query.get(id)
    if user:
        user.delete_from_db()
        return {"mensaje": "Usuario eliminado exitosamente"}, 200
    return {"mensaje": "Usuario no encontrado"}, 404

@user_bp.route('/users', methods=['GET'])
def get_users():
    users = UserModel.query.all()
    return {"users": [user.json() for user in users]}, 200
