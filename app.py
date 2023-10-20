from flask import Flask, request
from auth.jwt import Security
from api.auth.auth import auth_routes
from api.rol.api_rol import rol_bp
from api.user.api_user import user_bp
from api.product.api_product import product_bp
from api.package.api_package import package_bp
from api.production.api_production import production_bp
from api.payment.api_payment import payment_bp
from Config.db import app   

# Crear una instancia de la aplicación Flask
app = Flask(__name__)

# Registrar rutas y puntos finales de la API
app.register_blueprint(auth_routes, url_prefix='/api')
app.register_blueprint(rol_bp, url_prefix='/api')
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(product_bp, url_prefix='/api')
app.register_blueprint(package_bp, url_prefix='/api')
app.register_blueprint(production_bp, url_prefix='/api')
app.register_blueprint(payment_bp, url_prefix='/api')

# Ruta principal que muestra "Hola Mundo"
@app.route("/")
def index():
    return "Hola Mundo"

# Middleware que verifica tokens y roles antes de cada solicitud
@app.before_request
def token_middleware():
    current_route = request.path

    # Rutas excluidas que no requieren token de autenticación
    excluded_routes = ["/api/login"]

    # Rutas que no requieren rol de administrador
    no_admin_routes = ["/api/newproduction"]

    # Obtener el token del encabezado de la solicitud
    token = request.headers.get("Authorization")

    if token is None and current_route not in excluded_routes:
        return "No autorizado", 401
    else:
        token_data = Security.verify_token(request.headers)

        if current_route not in excluded_routes and not token_data['token_valid']:
            return "Token inválido", 401

        if (
            current_route not in no_admin_routes
            and token_data['role'] != 1
            and current_route not in excluded_routes
        ):
            return "Se requiere permisos de administrador", 401

# Iniciar la aplicación si se ejecuta directamente
if __name__ == "__main__":
    app.run(debug=True, port=5000, host='0.0.0.0')
