from datetime import datetime
from models.product import ProductModel
from models.production import ProductionModel
from models.package import PackageModel
from models.rol import RolModel 
from models.user import UserModel

def calculate_package_payment(compensation_role, amount, product_compensation):
    return amount*(compensation_role + product_compensation)
 
def create_production_and_package(user_id, product_id):
    active_package = PackageModel.query.filter_by(user_id=user_id, active=False).first()

    if active_package is None:
        package = PackageModel(date=datetime.now(), active=False, amount=1, user_id=user_id, payment=0)
        package.save_to_db()
    else:
        package = active_package

    # Obtener la compensación del rol del usuario desde la base de datos
    user = UserModel.query.get(user_id)
    user_rol_id = user.id_rol  # Supongo que el campo se llama id_rol en UserModel
    user_role = RolModel.query.get(user_rol_id)

    compensation_role = user_role.compensation if user_role else 0  # Valor predeterminado si no se encuentra un rol

    product = ProductModel.query.get(product_id)
    product_compensation = product.price if product else 0  # Valor predeterminado si no se encuentra el producto

    production = ProductionModel(date=datetime.now(), user_id=user_id, product_id=product_id, package_id=package.id)
    production.save_to_db()

    package.amount = ProductionModel.query.filter_by(user_id=user_id, package_id=package.id).count()
    package.payment = calculate_package_payment(compensation_role, package.amount, product_compensation)
    package.update_in_db()

    
    if package.amount % 12 == 0:
        package.active = True
        package.update_in_db()

    return production
