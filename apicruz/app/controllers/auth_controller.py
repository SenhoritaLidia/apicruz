from flask import request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash
from app.models.user import User

def login():
    data = request.get_json()

    email = data.get("email")
    senha = data.get("senha")

    usuario = User.query.filter_by(email=email).first()

    if usuario and check_password_hash(usuario.senha, senha):
        token = create_access_token(identity=usuario.id)

        return jsonify(access_token=token), 200

    return jsonify({"erro": "Email ou senha inválidos"}), 401