from flask import Blueprint, request
from Models.usuario import UsuarioModel
from Config.db import db

usuario_bp = Blueprint('usuario', __name__)

@usuario_bp.route('/usuarios', methods=['POST'])
def crear_usuario():
    data = request.get_json()
    nuevo_usuario = UsuarioModel(**data)
    nuevo_usuario.save_to_db()
    return {"mensaje": "Usuario creado exitosamente"}, 201

@usuario_bp.route('/usuarios/<int:id>', methods=['GET'])
def obtener_usuario(id):
    usuario = UsuarioModel.query.get(id)
    if usuario:
        return usuario.json(), 200
    return {"mensaje": "Usuario no encontrado"}, 404

@usuario_bp.route('/usuarios/<int:id>', methods=['PUT'])
def actualizar_usuario(id):
    usuario = UsuarioModel.query.get(id)
    if usuario:
        data = request.get_json()
        usuario.nombre = data['nombre']
        usuario.identificacion = data['identificacion']
        usuario.rol = data['rol']
        usuario.update_in_db()
        return {"mensaje": "Usuario actualizado exitosamente"}, 200
    return {"mensaje": "Usuario no encontrado"}, 404

@usuario_bp.route('/usuarios/<int:id>', methods=['DELETE'])
def eliminar_usuario(id):
    usuario = UsuarioModel.query.get(id)
    if usuario:
        usuario.delete_from_db()
        return {"mensaje": "Usuario eliminado exitosamente"}, 200
    return {"mensaje": "Usuario no encontrado"}, 404

@usuario_bp.route('/usuarios', methods=['GET'])
def obtener_todos_los_usuarios():
    usuarios = UsuarioModel.query.all()
    return {"usuarios": [usuario.json() for usuario in usuarios]}, 200
