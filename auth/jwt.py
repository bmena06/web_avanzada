import datetime
import pytz
import jwt

class Security():

    # Zona horaria utilizada para la generación y verificación de tokens
    timezone = pytz.timezone('America/Bogota')

    @classmethod
    def generate_token(cls, authenticate_user):
        """
        Genera un token JWT para autenticar a un usuario.

        Parámetros:
        - authenticate_user: El objeto del usuario autenticado del que se obtendrán los datos para el token.

        Retorna:
        - Un token JWT firmado que contiene información de autenticación, incluyendo el nombre y el rol del usuario.
        """

        # Crear el contenido del token (payload)
        payload = {
            "iat": datetime.datetime.now(tz=cls.timezone),  # Fecha de emisión
            "exp": datetime.datetime.now(tz=cls.timezone) + datetime.timedelta(days=1),  # Fecha de expiración
            'name': authenticate_user.name,  # Nombre del usuario
            'role': authenticate_user.id_rol,  # Rol del usuario
        }

        # Generar el token JWT con una clave secreta y el algoritmo HS256
        return jwt.encode(payload, "clavesecreta", algorithm="HS256")

    @classmethod
    def verify_token(cls, headers):
        """
        Verifica un token JWT proporcionado en las cabeceras de la solicitud.

        Parámetros:
        - headers: Las cabeceras de la solicitud HTTP.

        Retorna:
        - Un diccionario con dos claves:
          - 'token_valid': Un valor booleano que indica si el token es válido o no.
          - 'role': El rol del usuario si el token es válido, o None si es inválido.
        """

        if 'Authorization' in headers:
            authorization = headers['Authorization']

            # Extraer el token codificado del encabezado "Authorization"
            encoded_token = authorization.split(" ")[1][:-1]

            if encoded_token:
                try:
                    # Decodificar el token y verificar su validez
                    decoded_token = jwt.decode(
                        encoded_token, "clavesecreta", algorithms=["HS256"])

                    return {
                        "token_valid": True,
                        "role": decoded_token['role']
                    }
                except jwt.ExpiredSignatureError:
                    return {
                        "token_valid": False,
                        "role": None
                    }
                except jwt.InvalidTokenError:
                    return {
                        "token_valid": False,
                        "role": None
                    }

        # Devolver False si no se proporcionó un token válido en las cabeceras
        return {
            "token_valid": False,
            "role": None
        }
