from flask import request, jsonify
from models.user import UserModel
from auth.jwt import Security
from werkzeug.security import generate_password_hash, check_password_hash


class AuthService():
    def login_user(cls, email,password):
        user = UserModel.query.filter_by(email=email).first()
        password = UserModel.query.filter_by(password=password).first
        if user and password:
            token = Security.generate_token(user)
            return jsonify({"token": token, "user": user.json()})
        else:
            return False