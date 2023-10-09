from flask import Blueprint, request
from Models.paquete import PaqueteModel
from Config.db import db

paquete_bp = Blueprint('paquete', __name__)

@paquete_bp.route('/paquetes', methods=['POST'])
def crear_paquete():
    data = request.get_json()
    nuevo_paquete = PaqueteModel(**data)
    nuevo_paquete.save_to_db()
    return {"mensaje": "Paquete creado exitosamente"}, 201

@paquete_bp.route('/paquetes/<int:id>', methods=['GET'])
def obtener_paquete(id):
    paquete = PaqueteModel.query.get(id)
    if paquete:
        return paquete.json(), 200
    return {"mensaje": "Paquete no encontrado"}, 404

@paquete_bp.route('/paquetes/<int:id>', methods=['PUT'])
def actualizar_paquete(id):
    paquete = PaqueteModel.query.get(id)
    if paquete:
        data = request.get_json()
        paquete.fecha = data['fecha']
        paquete.total = data['total']
        paquete.valor = data['valor']
        paquete.update_in_db()
        return {"mensaje": "Paquete actualizado exitosamente"}, 200
    return {"mensaje": "Paquete no encontrado"}, 404

@paquete_bp.route('/paquetes/<int:id>', methods=['DELETE'])
def eliminar_paquete(id):
    paquete = PaqueteModel.query.get(id)
    if paquete:
        paquete.delete_from_db()
        return {"mensaje": "Paquete eliminado exitosamente"}, 200
    return {"mensaje": "Paquete no encontrado"}, 404

@paquete_bp.route('/paquetes', methods=['GET'])
def obtener_todos_los_paquetes():
    paquetes = PaqueteModel.query.all()
    return {"paquetes": [paquete.json() for paquete in paquetes]}, 200
