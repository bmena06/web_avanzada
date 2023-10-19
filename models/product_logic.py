from datetime import datetime
from models.production import ProductionModel
from models.package import PackageModel

def create_production_and_package(user_id, product_id):
    # Inicializa package a None para que esté definido incluso si no se encuentra un paquete activo
    package = None

    active_package = PackageModel.query.filter_by(user_id=user_id, active=True).first()

    if active_package is None:
        package = PackageModel(date=datetime.now(), active=True, compensation=0, user_id=user_id)
        package.save_to_db()
    else:
        production_count = ProductionModel.query.filter_by(user_id=user_id, product_id=product_id).count()
        if production_count % 12 == 0:
            package = PackageModel(date=datetime.now(), active=True, compensation=0, user_id=user_id)
            package.save_to_db()

    production = ProductionModel(date=datetime.now(), user_id=user_id, product_id=product_id, package_id=package.id if package is not None else None)
    production.save_to_db()

    if package is not None:
        production.package_id = package.id
        production.update_in_db()
