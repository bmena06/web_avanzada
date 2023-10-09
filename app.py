from flask import Flask
from api.usuario.api_usuario import usuario_bp
from api.producto.api_producto import producto_bp
from api.paquete.api_paquete import paquete_bp
from Config.db import app   


app.register_blueprint(usuario_bp, url_prefix='/api')
app.register_blueprint(producto_bp, url_prefix='/api')
app.register_blueprint(paquete_bp, url_prefix='/api')

@app.route("/")
def index():
    return "Hola Mundo"

if __name__ == "__main__":
    app.run(debug=True, port=5000, host='0.0.0.0')