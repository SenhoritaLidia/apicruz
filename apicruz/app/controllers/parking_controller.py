from app.extensions import db
from app.models.parking import Parking
from app.models.parking_spot import ParkingSpot
from app.schemas.parking_schema import ParkingSchema
from app.schemas.parking_spot_schema import ParkingSpotSchema
from app.utils.response import error_response, success_response


parking_schema = ParkingSchema()
parkings_schema = ParkingSchema(many=True)
parking_spot_schema = ParkingSpotSchema()
parking_spots_schema = ParkingSpotSchema(many=True)


def listar_parkings():
    parkings = Parking.query.all()
    return success_response(parkings_schema.dump(parkings))


def criar_parking(data):
    dados_validados = parking_schema.load(data)
    novo_parking = Parking(**dados_validados)

    db.session.add(novo_parking)
    db.session.commit()

    return success_response(parking_schema.dump(novo_parking), 201)


def listar_spots():
    spots = ParkingSpot.query.all()
    return success_response(parking_spots_schema.dump(spots))


def criar_spot(data):
    dados_validados = parking_spot_schema.load(data)

    parking = Parking.query.get(dados_validados["parking_id"])
    if parking is None:
        return error_response("Recurso não encontrado", 404)

    novo_spot = ParkingSpot(**dados_validados)

    db.session.add(novo_spot)
    db.session.commit()

    return success_response(parking_spot_schema.dump(novo_spot), 201)


def atualizar_spot(id, data):
    spot = ParkingSpot.query.get_or_404(id)

    dados_validados = parking_spot_schema.load(data, partial=True)
    for campo, valor in dados_validados.items():
        setattr(spot, campo, valor)

    db.session.commit()
    return success_response(parking_spot_schema.dump(spot))


def listar_spots_por_parking(parking_id):
    parking = Parking.query.get_or_404(parking_id)
    spots = parking.spots
    return success_response(parking_spots_schema.dump(spots))
