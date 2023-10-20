from Config.db import db, app, ma

# Definición del modelo de Payment en la base de datos
class PaymentModel(db.Model):
    __tablename__ = 'payment'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # ID del usuario asociado al pago
    total_payment = db.Column(db.Integer)  # Total del pago
    
    # Constructor para inicializar un objeto de pago
    def __init__(self, user_id, total_payment):
        self.user_id = user_id
        self.total_payment = total_payment

    # Guarda el objeto de pago en la base de datos
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # Actualiza el objeto de pago en la base de datos
    def update_in_db(self):
        db.session.commit()

    # Elimina el objeto de pago de la base de datos
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    # Serializa el objeto de pago a formato JSON
    def json(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'total_payment': self.total_payment
        }
    
# Crea la tabla en la base de datos según el modelo definido
with app.app_context():
    db.create_all()

# Definición del esquema de serialización para el objeto de pago
class PaymentSchema(ma.Schema):
    class Meta:
        fields = ('id', 'user_id', 'total_payment')
