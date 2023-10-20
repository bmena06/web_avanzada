from flask import Blueprint, request
from models.payment import PaymentModel  # Importa el modelo de pagos
from Config.db import db
from models.product_logic import create_production_and_package

payment_bp = Blueprint('payment', __name__)

@payment_bp.route('/payment/<int:id>', methods=['GET'])
def get_payment(id):
    payment = PaymentModel.query.get(id)
    if payment:
        return payment.json(), 200
    return {"mensaje": "Pago no encontrado"}, 404

@payment_bp.route('/updatepayment/<int:id>', methods=['PUT'])
def update_payment(id):
    payment = PaymentModel.query.get(id)
    if payment:
        data = request.get_json()
        payment.amount = data['amount']
        payment.update_in_db()  # Actualiza el pago en la base de datos
        return {"mensaje": "Pago actualizado exitosamente"}, 200
    return {"mensaje": "Pago no encontrado"}, 404

@payment_bp.route('/deletepayment/<int:id>', methods=['DELETE'])
def delete_payment(id):
    payment = PaymentModel.query.get(id)
    if payment:
        payment.delete_from_db()  # Elimina el pago de la base de datos
        return {"mensaje": "Pago eliminado exitosamente"}, 200
    return {"mensaje": "Pago no encontrado"}, 404

@payment_bp.route('/payments', methods=['GET'])
def get_payments():
    payments = PaymentModel.query.all()
    return {"payments": [payment.json() for payment in payments]}, 200
