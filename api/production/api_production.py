from flask import Blueprint, request
from models.production import ProductionModel
from Config.db import db

production_bp = Blueprint('production', __name__)

@production_bp.route('/newproduction', methods=['POST'])
def create_production():
    data = request.get_json()
    new_production = ProductionModel(**data)
    new_production.save_to_db()
    return {"mensaje": "Produccion creada exitosamente"}, 201

@production_bp.route('/production/<int:id>', methods=['GET'])
def get_production(id):
    production = ProductionModel.query.get(id)
    if production:
        return production.json(), 200
    return {"mensaje": "Produccion no encontrada"}, 404

@production_bp.route('/updateproduction/<int:id>', methods=['PUT'])
def update_production(id):
    production = ProductionModel.query.get(id)
    if production:
        data = request.get_json()
        production.name = data['nombre']
        production.email = data['identificacion']
        production.update_in_db()
        return {"mensaje": "Produccion actualizado exitosamente"}, 200
    return {"mensaje": "Produccion no encontrada"}, 404

@production_bp.route('/deleteproduction/<int:id>', methods=['DELETE'])
def delete_production(id):
    production = ProductionModel.query.get(id)
    if production:
        production.delete_from_db()
        return {"mensaje": "Produccion eliminado exitosamente"}, 200
    return {"mensaje": "Produccion no encontrada"}, 404

@production_bp.route('/productions', methods=['GET'])
def get_productions():
    productions = ProductionModel.query.all()
    return {"productions": [production.json() for production in productions]}, 200
