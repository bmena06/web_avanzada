from Config.db import db, app, ma

class ProductionModel(db.Model):
    __tablename__ = 'production'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(30))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    package_id = db.Column(db.Integer, db.ForeignKey('package.id'))
    
    def __init__(self, date, user_id, product_id, package_id):
        """
        Inicializa una instancia de ProductionModel con una fecha, ID de usuario, ID de producto y ID de paquete.

        Args:
            date (str): La fecha de la producción.
            user_id (int): El ID del usuario asociado a la producción.
            product_id (int): El ID del producto asociado a la producción.
            package_id (int): El ID del paquete asociado a la producción.
        """
        self.date = date
        self.user_id = user_id
        self.product_id = product_id
        self.package_id = package_id

    def save_to_db(self):
        """
        Guarda el objeto ProductionModel en la base de datos.
        """
        db.session.add(self)
        db.session.commit()
    
    def update_in_db(self):
        """
        Actualiza el objeto ProductionModel en la base de datos.
        """
        db.session.commit()
    
    def delete_from_db(self):
        """
        Elimina el objeto ProductionModel de la base de datos.
        """
        db.session.delete(self)
        db.session.commit()
    
    def json(self):
        """
        Retorna una representación JSON del objeto ProductionModel.

        Returns:
            dict: Un diccionario que contiene los campos de la producción en formato JSON.
        """
        return {
            'id': self.id,
            'date': self.date,
            'user_id': self.user_id,
            'product_id': self.product_id,
            'package_id': self.package_id
        }

with app.app_context():
    db.create_all()

class ProductionSchema(ma.Schema):
    class Meta:
        fields = ('id', 'date', 'user_id', 'product_id', 'package_id')
