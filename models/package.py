from Config.db import db,app,ma

class PackageModel(db.Model):
    __tablename__ = 'package'
    
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date)
    total = db.Column(db.Integer)
    valor = db.Column(db.DECIMAL(10, 2))
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    
    def __init__(self, fecha, total, valor, user_id, product_id):
        self.fecha = fecha
        self.total = total
        self.valor = valor
        self.user_id = user_id
        self.product_id = product_id

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
            'user_id': self.user_id,
            'product_id': self.product_id
        }

with app.app_context():
    db.create_all()

class PackageSchema(ma.Schema):
    class Meta:
        fields = ('id', 'fecha','total','valor','user_id','product_id')
