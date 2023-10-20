from Config.db import db, app, ma

# Definición del modelo de Package en la base de datos
class PackageModel(db.Model):
    __tablename__ = 'package'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)  # Fecha del paquete
    active = db.Column(db.Boolean)  # Estado del paquete (activo/inactivo)
    amount = db.Column(db.Integer)  # Cantidad de elementos en el paquete
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # ID del usuario al que pertenece el paquete
    
    # Constructor para inicializar un objeto de paquete
    def __init__(self, date, active, amount, user_id):
        self.date = date
        self.active = active
        self.amount = amount
        self.user_id = user_id

    # Guarda el objeto de paquete en la base de datos
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    # Actualiza el objeto de paquete en la base de datos
    def update_in_db(self):
        db.session.commit()
    
    # Elimina el objeto de paquete de la base de datos
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
    
    # Serializa el objeto de paquete a formato JSON
    def json(self):
        return {
            'id': self.id,
            'date': self.date,
            'active': self.active,
            'amount': self.amount,
            'user_id': self.user_id
        }

# Crea las tablas en la base de datos según los modelos definidos
with app.app_context():
    db.create_all()

# Definición del esquema de serialización para el objeto de paquete
class PackageSchema(ma.Schema):
    class Meta:
        fields = ('id', 'date', 'active', 'amount', 'user_id')

