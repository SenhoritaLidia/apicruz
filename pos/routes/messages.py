from flask import Blueprint, jsonify

messages_bp = Blueprint("messages", __name__)

@messages_bp.route("/", methods=["GET"])
def listar_mensagens():
    return jsonify({
        "mensagens": [
            "Primeira mensagem",
            "Segunda mensagem"
        ]
    })