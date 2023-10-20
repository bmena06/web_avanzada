from Config.db import db, app, ma

class RolModel(db.Model):
    __tablename__ = 'rol'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    compensation = db.Column(db.Integer)
    
    def __init__(self, name, compensation):
        """
        Inicializa una instancia de RolModel con un nombre y compensación.

        Args:
            name (str): El nombre del rol.
            compensation (int): La compensación asociada al rol.
        """
        self.name = name
        self.compensation = compensation

    def save_to_db(self):
        """
        Guarda el objeto RolModel en la base de datos.
        """
        db.session.add(self)
        db.session.commit()
    
    def update_in_db(self):
        """
        Actualiza el objeto RolModel en la base de datos.
        """
        db.session.commit()
    
    def delete_from_db(self):
        """
        Elimina el objeto RolModel de la base de datos.
        """
        db.session.delete(self)
        db.session.commit()
    
    def json(self):
        """
        Retorna una representación JSON del objeto RolModel.

        Returns:
            dict: Un diccionario que contiene los campos del rol en formato JSON.
        """
        return {
            'id': self.id,
            'name': str(self.name),
            'compensation': self.compensation
        }

with app.app_context():
    db.create_all()

class RolSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'compensation')
