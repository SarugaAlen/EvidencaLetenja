from fastapi.testclient import TestClient
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from main import app  

client = TestClient(app)


# 1. Test creating a new pilot (POST /dodajPilota/)
def test_create_pilot():
    # Data to send in the request
    pilot_data = {
        "ime": "Janez",
        "priimek": "Novak"
    }

    # Send a POST request to create a new pilot
    response = client.post("/dodajPilota/", json=pilot_data)

    # Check if the response status code is 200 OK
    assert response.status_code == 200

    # Check if the response contains the expected data
    data = response.json()
    assert "idPilot" in data
    assert data["ime"] == pilot_data["ime"]
    assert data["priimek"] == pilot_data["priimek"]


def test_read_pilots():
    pilot_data = {
        "ime": "Miha",
        "priimek": "Kovac"
    }
    client.post("/dodajPilota/", json=pilot_data)

    response = client.get("/pridobiPilote/")

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0  

    assert any(pilot["ime"] == pilot_data["ime"] and pilot["priimek"] == pilot_data["priimek"] for pilot in data)


def test_delete_pilot():

    pilot_data = {
        "ime": "Andrej",
        "priimek": "Zajc"
    }
    create_response = client.post("/dodajPilota/", json=pilot_data)
    created_pilot_id = create_response.json()["idPilot"]

    response = client.delete(f"/pilot/{created_pilot_id}")

    assert response.status_code == 200
    assert response.json() == {"message": "Pilot deleted successfully"}

    response = client.get(f"/pilot/{created_pilot_id}")
    assert response.status_code == 404  # The pilot should no longer exist


