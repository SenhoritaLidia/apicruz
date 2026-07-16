import unittest

from app import create_app
from app.extensions import db


class ParkingApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config.update(TESTING=True)
        self.client = self.app.test_client()

        with self.app.app_context():
            db.drop_all()
            db.create_all()

    def test_parking_and_spot_flow(self):
        parking_response = self.client.post(
            "/parkings/",
            json={"nome": "Estacionamento Central", "endereco": "Rua A, 123"},
        )
        self.assertEqual(parking_response.status_code, 201)
        parking_data = parking_response.get_json()
        self.assertTrue(parking_data["success"])
        self.assertEqual(parking_data["data"]["nome"], "Estacionamento Central")

        list_parking_response = self.client.get("/parkings/")
        self.assertEqual(list_parking_response.status_code, 200)
        self.assertEqual(len(list_parking_response.get_json()["data"]), 1)

        spot_response = self.client.post(
            "/spots/",
            json={"codigo": "A1", "ocupada": False, "parking_id": parking_data["data"]["id"]},
        )
        self.assertEqual(spot_response.status_code, 201)
        spot_data = spot_response.get_json()
        self.assertTrue(spot_data["success"])
        self.assertEqual(spot_data["data"]["codigo"], "A1")
        self.assertFalse(spot_data["data"]["ocupada"])

        list_spots_response = self.client.get("/spots/")
        self.assertEqual(list_spots_response.status_code, 200)
        self.assertEqual(len(list_spots_response.get_json()["data"]), 1)

        update_response = self.client.patch(
            f"/spots/{spot_data['data']['id']}",
            json={"ocupada": True},
        )
        self.assertEqual(update_response.status_code, 200)
        self.assertTrue(update_response.get_json()["data"]["ocupada"])

        spots_by_parking = self.client.get(f"/parkings/{parking_data['data']['id']}/spots")
        self.assertEqual(spots_by_parking.status_code, 200)
        self.assertEqual(len(spots_by_parking.get_json()["data"]), 1)

        invalid_spot_response = self.client.post(
            "/spots/",
            json={"codigo": "B1", "ocupada": False, "parking_id": 999},
        )
        self.assertEqual(invalid_spot_response.status_code, 404)
        self.assertFalse(invalid_spot_response.get_json()["success"])


if __name__ == "__main__":
    unittest.main()
