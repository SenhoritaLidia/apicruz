from flask import request
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash

from app.models.user import User


def login():
    data = request.get_json()

    usuario = User.query.filter_by(email=data["email"]).first()

    if not usuario:
        return {"erro": "Usuário ou senha inválidos"}, 401

    if not check_password_hash(usuario.senha, data["senha"]):
        return {"erro": "Usuário ou senha inválidos"}, 401

    token = create_access_token(identity=str(usuario.id))

    return {
        "access_token": token
    }, 200