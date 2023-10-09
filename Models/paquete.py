from Config.db import db,app,ma

class PaqueteModel(db.Model):
    __tablename__ = 'paquete'
    
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date)
    total = db.Column(db.Integer)
    valor = db.Column(db.DECIMAL(10, 2))
    
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'))
    
    def __init__(self, fecha, total, valor, usuario_id, producto_id):
        self.fecha = fecha
        self.total = total
        self.valor = valor
        self.usuario_id = usuario_id
        self.producto_id = producto_id

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
            'fecha': str(self.fecha),
            'total': self.total,
            'valor': float(self.valor),
            'usuario_id': self.usuario_id,
            'producto_id': self.producto_id
        }

with app.app_context():
    db.create_all()

class PaqueeteSchema(ma.Schema):
    class Meta:
        fields = ('id', 'fecha','total','valor','usuario_id','producto_id')
