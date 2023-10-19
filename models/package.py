from Config.db import db,app,ma

class PackageModel(db.Model):
    __tablename__ = 'package'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    active = db.Column(db.Boolean)
    compesation = db.Column(db.DECIMAL(10, 2))
    
    def __init__(self, date, active, compesation):
        self.date = date
        self.active = active
        self.compensation = compesation


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
            'active': self.total,
            'compesation': self.valor,
        }

with app.app_context():
    db.create_all()

class PackageSchema(ma.Schema):
    class Meta:
        fields = ('id', 'fecha','total','valor','user_id','product_id')
