from flask import request, jsonify, Blueprint
from auth.auth import AuthService
auth_routes = Blueprint("auth_routes", __name__)
auth_service = AuthService()


@auth_routes.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    name = data.get("name")
    password = data.get("password")
    response = auth_service.login_user(name, password)
    if response:
        return response, 200
    else:
        return "Usuario o contraseña incorrecta", 401