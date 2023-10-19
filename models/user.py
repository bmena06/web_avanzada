from Config.db import db, app ,ma

class UserModel(db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    email = db.Column(db.String(30))
    password = db.Column(db.String(30))
    id_rol = db.Column(db.Integer,db.ForeignKey('rol.id'))
    
    def __init__(self, name, email,password,id_rol):
        self.name = name
        self.email = email
        self.password = password
        self.id_rol = id_rol

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
            'email': self.email,
            'password': self.password,
            'id_rol': self.id_rol
        }

with app.app_context():
    db.create_all()

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name','email','password','id_rol')
