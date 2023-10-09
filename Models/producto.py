from Config.db import ma, db, app

class ProductoModel(db.Model):
    __tablename__ = 'producto'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))
    numero = db.Column(db.Integer)
    
    def __init__(self, nombre, numero):
        self.nombre = nombre
        self.numero = numero

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def update_in_db(self):
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'numero': self.numero
        }

with app.app_context():
    db.create_all()

class ProductoSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nombre','numero')
