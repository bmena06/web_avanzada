from Config.db import db,app,ma

class RolModel(db.Model):
    __tablename__ = 'rol'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    compensation = db.Column(db.Integer)
    
    
    def __init__(self, name, compensation):
        self.name = name
        self.compensation = compensation

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
            'name': str(self.name),
            'compensation': self.compensation,
  
        }

with app.app_context():
    db.create_all()

class RolSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name','compensation')
