from Config.db import db,app,ma

class PackageModel(db.Model):
    __tablename__ = 'package'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    compensation = db.Column(db.DECIMAL(10, 2))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __init__(self, date, compensation, user_id):
        self.date = date
        self.compensation = compensation
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
            'compensation': self.compensation,
            'user_id': self.user_id
        }

with app.app_context():
    db.create_all()

class PackageSchema(ma.Schema):
    class Meta:
        fields = ('id', 'date','compensation','user_id')
