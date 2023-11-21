from flask import request, jsonify, Blueprint
from auth.auth import AuthService

auth_routes = Blueprint("auth_routes", __name__)
auth_service = AuthService()

@auth_routes.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    name = data.get("name")
    password = data.get("password")
    print("name: ", name,"password: ", password)
    # Llamar al método de AuthService para iniciar sesión del usuario
    response = auth_service.login_user(name, password)
    if response:
        # Si el inicio de sesión es exitoso, agrega el token al diccionario de respuesta
        response_dict = response.get_json()
        # Devuelve el diccionario completo en formato JSON
        return jsonify(response_dict), 200
    else:
        # Si el inicio de sesión falla debido a credenciales incorrectas, retorna un mensaje de error en JSON
        return jsonify({"message": "Usuario o contraseña incorrecta"}), 401
