from datetime import datetime
from models.production import ProductionModel
from models.package import PackageModel

def create_production_and_package(user_id, product_id):
    active_package = PackageModel.query.filter_by(user_id=user_id, active=False).first()

    if active_package is None:
        package = PackageModel(date=datetime.now(), active=False, compensation=0, amount=1, user_id=user_id)
        package.save_to_db()
    else:
        package = active_package

    production = ProductionModel(date=datetime.now(), user_id=user_id, product_id=product_id, package_id=package.id)
    production.save_to_db()

    package.amount = ProductionModel.query.filter_by(user_id=user_id, package_id=package.id).count()
    package.update_in_db()
    
    if package.amount % 12 == 0:
        package.active = True
        package.update_in_db()

    return production