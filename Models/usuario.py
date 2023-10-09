from Config.db import db, app ,ma

class UsuarioModel(db.Model):
    __tablename__ = 'usuario'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))
    identificacion = db.Column(db.String(255))
    rol = db.Column(db.String(255))
    
    def __init__(self, nombre, identificacion, rol):
        self.nombre = nombre
        self.identificacion = identificacion
        self.rol = rol

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
            'identificacion': self.identificacion,
            'rol': self.rol
        }

with app.app_context():
    db.create_all()

class UsuarioSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nombre','identificacion', 'rol')
