from flask import Blueprint, jsonify, request

from flask_jwt_extended import jwt_required

from app.controllers.parking_controller import (
    atualizar_spot,
    criar_spot,
    listar_spots,
)

spots_bp = Blueprint("spots", __name__)


@spots_bp.route("/", methods=["GET"])
def get_spots():
    response, status = listar_spots()
    return jsonify(response), status


@spots_bp.route("/", methods=["POST"])
@jwt_required()
def post_spot():
    data = request.get_json()
    response, status = criar_spot(data)
    return jsonify(response), status


@spots_bp.route("/<int:id>", methods=["PATCH"])
@jwt_required()
def patch_spot(id):
    response, status = atualizar_spot(id, request.get_json())
    return jsonify(response), status
