from Config.db import db,app,ma

class ProductionModel(db.Model):
    __tablename__ = 'production'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(30))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    package_id = db.Column(db.Integer, db.ForeignKey('package.id'))

    
    def __init__(self, date, user_id, product_id, package_id):
        self.date = date
        self.user_id = user_id
        self.product_id = product_id
        self.package_id = package_id

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
            'date': str(self.fecha),
            'user_id': self.total,
            'product_id': self.valor,
            'package_id': self.usuario_id,
        }

with app.app_context():
    db.create_all()

class ProductionSchema(ma.Schema):
    class Meta:
        fields = ('id', 'date','user_id','product_id','package_id')
