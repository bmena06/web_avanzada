from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
CORS(app)
cors = CORS(app, resources={r"/api/*": {"origins": "http://localhost:4200"}})

#creamos las credenciales para conectarnos a la bd
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/web_avanzada'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = "WebAvanzada"

#creamos los objetos de bd

db = SQLAlchemy(app)
ma = Marshmallow(app)