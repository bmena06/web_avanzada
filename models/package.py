from Config.db import db,app,ma

class PackageModel(db.Model):
    __tablename__ = 'package'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    active = db.Column(db.Boolean)
    amount = db.Column(db.Integer)
    payment = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __init__(self, date,active,amount,payment,user_id):
        self.date = date
        self.active = active
        self.amount = amount
        self.payment = payment
        self.user_id = user_id

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
            'date': self.date,
            'active': self.active,
            'amount': self.amount,
            'payment': self.payment,
            'user_id': self.user_id
        }

with app.app_context():
    db.create_all()

class PackageSchema(ma.Schema):
    class Meta:
        fields = ('id', 'date','active','amount','payment','user_id')
