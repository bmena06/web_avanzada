from flask import Flask
from api.rol.api_rol import rol_bp
from api.user.api_user import user_bp
from api.product.api_product import product_bp
from api.package.api_package import package_bp
from api.production.api_production import production_bp
from Config.db import app   

app.register_blueprint(rol_bp, url_prefix='/api')
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(product_bp, url_prefix='/api')
app.register_blueprint(package_bp, url_prefix='/api')
app.register_blueprint(production_bp, url_prefix='/api')


@app.route("/")
def index():
    return "Hola Mundo"

if __name__ == "__main__":
    app.run(debug=True, port=5000, host='0.0.0.0')