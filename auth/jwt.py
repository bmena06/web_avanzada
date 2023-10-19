import datetime
import pytz
import jwt


class Security():

    timezone = pytz.timezone('America/Bogota')

    @classmethod
    def generate_token(cls, authenticate_user):

        payload = {
            "iat": datetime.datetime.now(tz=cls.timezone),
            "exp": datetime.datetime.now(tz=cls.timezone) + datetime.timedelta(days=1),
            'name': authenticate_user.name,
            'role': authenticate_user.id_rol,
        }

        return jwt.encode(payload, "clavesecreta", algorithm="HS256")

    @classmethod
    def verify_token(cls, headers):
        if 'Authorization' in headers:
            authorization = headers['Authorization']

            encoded_token = authorization.split(" ")[1][:-1]

            if encoded_token:
                try:
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

        return {
            "token_valid": False,
            "role": None
        }