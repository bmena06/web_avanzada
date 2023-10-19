from Config.db import ma, db, app

class ProductModel(db.Model):
    __tablename__ = 'product'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    price = db.Column(db.Integer)
    
    def __init__(self, name, price):
        self.name = name
        self.price = price

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
            'name': self.name,
            'price': self.price
        }

with app.app_context():
    db.create_all()

class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name','price')
