from Config.db import db,app,ma

class PaymentModel(db.Model):
    __tablename__ = 'payment'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    total_payment = db.Column(db.Integer)
    
    def __init__(self, user_id, total_payment):
        self.user_id = user_id
        self.total_payment = total_payment

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
            'user_id': self.user_id,
            'total_payment': self.total_payment
        }
    
with app.app_context():
    db.create_all()


class PaymentSchema(ma.Schema):
    class Meta:
        fields = ('id', 'user_id','product_id','total_payment')
