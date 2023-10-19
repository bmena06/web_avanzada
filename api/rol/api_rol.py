from flask import Blueprint, request
from models.rol import RolModel
from Config.db import db

rol_bp = Blueprint('rol', __name__)

@rol_bp.route('/newrol', methods=['POST'])
def create_rol():
    data = request.get_json()
    new_rol = RolModel(**data)
    new_rol.save_to_db()
    return {"mensaje": "Rol creado exitosamente"}, 201

@rol_bp.route('/rol/<int:id>', methods=['GET'])
def get_rol(id):
    rol = RolModel.query.get(id)
    if rol:
        return rol.json(), 200
    return {"mensaje": "Rol no encontrado"}, 404

@rol_bp.route('/updaterol/<int:id>', methods=['PUT'])
def update_rol(id):
    rol = RolModel.query.get(id)
    if rol:
        data = request.get_json()
        rol.name = data['nombre']
        rol.compensation = data['compensation']
        rol.update_in_db()
        return {"mensaje": "Rol actualizado exitosamente"}, 200
    return {"mensaje": "Rol no encontrado"}, 404

@rol_bp.route('/deleterol/<int:id>', methods=['DELETE'])
def delete_rol(id):
    rol = RolModel.query.get(id)
    if rol:
        rol.delete_from_db()
        return {"mensaje": "Rol eliminado exitosamente"}, 200
    return {"mensaje": "Rol no encontrado"}, 404

@rol_bp.route('/rols', methods=['GET'])
def get_rols():
    rols = RolModel.query.all()
    return {"rols": [rol.json() for rol in rols]}, 200
