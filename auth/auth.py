from flask import request, jsonify
from models.user import UserModel
from auth.jwt import Security
from werkzeug.security import generate_password_hash, check_password_hash

class AuthService():
    @classmethod
    def login_user(cls, email, password):
        """
        Método para autenticar a un usuario y generar un token JWT.

        Parámetros:
        - email (str): El correo electrónico del usuario.
        - password (str): La contraseña del usuario.

        Retorna:
        - Si la autenticación es exitosa, se genera un token JWT y se devuelve en formato JSON.
        - Si la autenticación falla, se devuelve False.
        """

        # Buscar al usuario por su correo electrónico
        user = UserModel.query.filter_by(email=email).first()

        # Comprobar si se encontró un usuario y si la contraseña coincide
        if user and check_password_hash(user.password, password):
            # Generar un token JWT para el usuario
            token = Security.generate_token(user)

            # Devolver el token y los datos del usuario en formato JSON
            return jsonify({"token": token, "user": user.json()})
        else:
            # Devolver False en caso de autenticación fallida
            return False
