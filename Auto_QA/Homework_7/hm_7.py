import pytest
import requests


class BookingApi:

    def __init__(self, url):
        self.url = url

    def create_token(self):
        response = requests.post(
            self.url + "/auth",
            json={
                "username": "admin",
                "password": "password123"
            }
        )

        return response

    def create_booking(self, booking_data):
        response = requests.post(
            self.url + "/booking",
            json=booking_data
        )

        return response

    def get_booking(self, booking_id):
        response = requests.get(
            self.url + f"/booking/{booking_id}"
        )

        return response

    def partial_update_booking(
        self,
        booking_id,
        update_data,
        token
    ):
        response = requests.patch(
            self.url + f"/booking/{booking_id}",
            json=update_data,
            headers={
                "Cookie": f"token={token}"
            }
        )

        return response


@pytest.fixture
def booking_api():
    base_url = "https://restful-booker.herokuapp.com"

    return BookingApi(base_url)


@pytest.fixture
def booking_data():
    return {
        "firstname": "Anton",
        "lastname": "Samoilenko",
        "totalprice": 150,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2026-10-10",
            "checkout": "2026-10-15"
        },
        "additionalneeds": "Breakfast"
    }


def test_create_booking(
    booking_api,
    booking_data
):
    response = booking_api.create_booking(
        booking_data
    )

    assert response.status_code == 200


def test_get_booking(
    booking_api,
    booking_data
):
    create_response = booking_api.create_booking(
        booking_data
    )

    created_booking = create_response.json()

    booking_id = created_booking["bookingid"]

    response = booking_api.get_booking(
        booking_id
    )

    assert response.status_code == 200


def test_partial_update_booking(
    booking_api,
    booking_data
):
    create_response = booking_api.create_booking(
        booking_data
    )

    created_booking = create_response.json()

    booking_id = created_booking["bookingid"]

    token_response = booking_api.create_token()

    token = token_response.json()["token"]

    update_data = {
        "firstname": "Michael"
    }

    response = booking_api.partial_update_booking(
        booking_id,
        update_data,
        token
    )

    assert response.status_code == 200


def test_get_nonexistent_booking(
    booking_api
):
    response = booking_api.get_booking(
        999999999
    )

    assert response.status_code == 404