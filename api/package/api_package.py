from flask import Blueprint, request
from models.package import PackageModel
from Config.db import db

package_bp = Blueprint('package', __name__)

@package_bp.route('/newpackage', methods=['POST'])
def create_package():
    data = request.get_json()
    new_package = PackageModel(**data)
    new_package.save_to_db()
    return {"mensaje": "Paquete creado exitosamente"}, 201

@package_bp.route('/package/<int:id>', methods=['GET'])
def get_package(id):
    package = PackageModel.query.get(id)
    if package:
        return package.json(), 200
    return {"mensaje": "Paquete no encontrado"}, 404

@package_bp.route('/updatepackage/<int:id>', methods=['PUT'])
def update_package(id):
    package = PackageModel.query.get(id)
    if package:
        data = request.get_json()
        package.date = data['date']
        package.active = data['active']
        package.amount = data ['amount']
        package.payment = data ['payment']
        package.update_in_db()
        return {"mensaje": "Paquete actualizado exitosamente"}, 200
    return {"mensaje": "Paquete no encontrado"}, 404

@package_bp.route('/deletepackage/<int:id>', methods=['DELETE'])
def delete_package(id):
    package = PackageModel.query.get(id)
    if package:
        package.delete_from_db()
        return {"mensaje": "Paquete eliminado exitosamente"}, 200
    return {"mensaje": "Paquete no encontrado"}, 404

@package_bp.route('/packages', methods=['GET'])
def get_packages():
    packages = PackageModel.query.all()
    return {"packages": [package.json() for package in packages]}, 200
