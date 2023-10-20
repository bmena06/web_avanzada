from datetime import datetime
from models.payment import PaymentModel
from models.product import ProductModel
from models.production import ProductionModel
from models.package import PackageModel
from models.rol import RolModel
from models.user import UserModel

# Función para crear una producción y gestionar el pago
def create_production_and_package(user_id, product_id):
    # Obtener o crear un paquete activo para el usuario
    active_package = PackageModel.query.filter_by(user_id=user_id, active=False).first()

    if active_package is None:
        package = PackageModel(date=datetime.now(), active=False, amount=1, user_id=user_id)
        package.save_to_db()
    else:
        package = active_package

    # Crear una nueva producción y asociarla al paquete
    production = ProductionModel(date=datetime.now(), user_id=user_id, product_id=product_id, package_id=package.id)
    production.save_to_db()

    # Actualizar la cantidad de producciones en el paquete
    package.amount = ProductionModel.query.filter_by(user_id=user_id, package_id=package.id).count()
    package.update_in_db()

    # Marcar el paquete como activo si se completa
    if package.amount % 12 == 0:
        package.active = True
        package.update_in_db()

    # Calcular el pago y actualizar o crear un registro de pago
    payment_amount = calculate_payment(user_id, product_id)
    existing_payment = PaymentModel.query.filter_by(user_id=user_id).first()
    
    if existing_payment:
        existing_payment.total_payment = payment_amount
        existing_payment.update_in_db()
    else:
        payment = PaymentModel(user_id=user_id, total_payment=payment_amount)
        payment.save_to_db()

    return production

# Función para calcular el pago
def calculate_payment(user_id, product_id):
    # Obtener la compensación del rol del usuario y el precio del producto
    user = UserModel.query.get(user_id)
    user_rol_id = user.id_rol
    user_role = RolModel.query.get(user_rol_id)
    compensation_role = user_role.compensation

    product = ProductModel.query.get(product_id)
    product_compensation = product.price 

    # Obtener el número de producciones realizadas por el usuario
    production_count = ProductionModel.query.filter_by(user_id=user_id).count()

    # Obtener el número de paquetes activos realizados por el usuario
    package_count = PackageModel.query.filter_by(user_id=user_id, active=True).count()

    # Calcular el monto total del pago
    total_payment = (compensation_role + product_compensation) * production_count + (1000 * package_count)

    return total_payment
