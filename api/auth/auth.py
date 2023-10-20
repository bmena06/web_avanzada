from flask import request, jsonify, Blueprint
from auth.auth import AuthService

# Crear un Blueprint para las rutas de autenticación
auth_routes = Blueprint("auth_routes", __name__)

# Crear una instancia de AuthService
auth_service = AuthService()

@auth_routes.route("/login", methods=["POST"])
def login():
    """
    Ruta de inicio de sesión que maneja las solicitudes POST de inicio de sesión.

    Parámetros:
    - Ninguno directamente desde la URL, pero se espera un cuerpo JSON con los siguientes campos:
      - "name": Nombre de usuario
      - "password": Contraseña

    Retorna:
    - Una respuesta JSON con un token de autenticación y los datos del usuario si el inicio de sesión es exitoso.
    - Un mensaje de error y código de estado 401 si el inicio de sesión falla debido a credenciales incorrectas.

    Esta ruta permite a los usuarios iniciar sesión proporcionando su nombre de usuario y contraseña.
    Si las credenciales son correctas, se genera un token de autenticación y se devuelve junto con los datos del usuario.
    Si las credenciales son incorrectas, se devuelve un mensaje de error y se establece un código de estado 401.
    """
    data = request.get_json()
    name = data.get("name")
    password = data.get("password")

    # Llamar al método de AuthService para iniciar sesión del usuario
    response = auth_service.login_user(name, password)

    if response:
        # Si el inicio de sesión es exitoso, retornar el token y los datos del usuario
        return response, 200
    else:
        # Si el inicio de sesión falla debido a credenciales incorrectas, retornar un mensaje de error
        return "Usuario o contraseña incorrecta", 401
