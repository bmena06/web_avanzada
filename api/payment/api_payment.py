from flask import Blueprint, request
from models.payment import PaymentModel  # Importa el modelo de pagos
from Config.db import db
from models.product_logic import create_production_and_package
from models.user import UserModel

# Crea un Blueprint para las rutas relacionadas con los pagos
payment_bp = Blueprint('payment', __name__)

@payment_bp.route('/payment/<int:id>', methods=['GET'])
def get_payment(id):
    """
    Ruta para obtener los detalles de un pago específico por su ID.

    Parámetros:
    - id: El ID del pago que se desea recuperar.

    Retorna:
    - Los datos del pago en formato JSON y código de estado 200 si se encuentra.
    - Un mensaje de error y código de estado 404 si el pago no se encuentra.

    Esta ruta permite recuperar los detalles de un pago específico proporcionando su ID.
    Si el pago se encuentra en la base de datos, se retornan sus datos en formato JSON.
    Si el pago no se encuentra, se devuelve un mensaje de error y se establece un código de estado 404.
    """
    payment = PaymentModel.query.get(id)
    if payment:
        return payment.json(), 200
    return {"mensaje": "Pago no encontrado"}, 404

@payment_bp.route('/updatepayment/<int:id>', methods=['PUT'])
def update_payment(id):
    """
    Ruta para actualizar los detalles de un pago específico por su ID mediante una solicitud PUT.

    Parámetros:
    - id: El ID del pago que se desea actualizar.
    - Se espera un cuerpo JSON con los datos actualizados del pago.

    Retorna:
    - Un mensaje de éxito y código de estado 200 si el pago se actualiza exitosamente.
    - Un mensaje de error y código de estado 404 si el pago no se encuentra.

    Esta ruta permite actualizar los detalles de un pago específico proporcionando su ID y los datos actualizados en el cuerpo de la solicitud.
    Si el pago se encuentra en la base de datos, se actualizan sus datos y se responde con un mensaje de éxito.
    Si el pago no se encuentra, se devuelve un mensaje de error y se establece un código de estado 404.
    """
    payment = PaymentModel.query.get(id)
    if payment:
        data = request.get_json()
        payment.amount = data['amount']
        payment.update_in_db()  # Actualiza el pago en la base de datos
        return {"mensaje": "Pago actualizado exitosamente"}, 200
    return {"mensaje": "Pago no encontrado"}, 404

@payment_bp.route('/deletepayment/<int:id>', methods=['DELETE'])
def delete_payment(id):
    """
    Ruta para eliminar un pago específico por su ID mediante una solicitud DELETE.

    Parámetros:
    - id: El ID del pago que se desea eliminar.

    Retorna:
    - Un mensaje de éxito y código de estado 200 si el pago se elimina exitosamente.
    - Un mensaje de error y código de estado 404 si el pago no se encuentra.

    Esta ruta permite eliminar un pago específico proporcionando su ID.
    Si el pago se encuentra en la base de datos, se elimina y se responde con un mensaje de éxito.
    Si el pago no se encuentra, se devuelve un mensaje de error y se establece un código de estado 404.
    """
    payment = PaymentModel.query.get(id)
    if payment:
        payment.delete_from_db()  # Elimina el pago de la base de datos
        return {"mensaje": "Pago eliminado exitosamente"}, 200
    return {"mensaje": "Pago no encontrado"}, 404

@payment_bp.route('/payments', methods=['GET'])
def get_payments():
    """
    Ruta para obtener una lista de todos los pagos con detalles de usuario.

    Retorna:
    - Una lista de todos los pagos con detalles de usuario en formato JSON y código de estado 200.

    Esta ruta permite recuperar una lista de todos los pagos disponibles en la base de datos con detalles de usuario.
    Los datos de los pagos se devuelven en formato JSON como una lista, incluyendo el nombre del usuario.
    """
    payments = PaymentModel.query.join(UserModel).add_columns(UserModel.name.label('user_name')).all()

    payment_list = []
    for payment, user_name in payments:
        payment_data = payment.json()
        payment_data['user_name'] = user_name
        payment_list.append(payment_data)

    return {"payments": payment_list}, 200
