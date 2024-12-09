from fastapi.testclient import TestClient
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from main import app  

client = TestClient(app)


def test_create_pilot():

    pilot_data = {
        "ime": "Janez",
        "priimek": "Novak"
    }

    response = client.post("/dodajPilota/", json=pilot_data)

    assert response.status_code == 200

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


def test_get_non_existent_pilot():
    response = client.get("/pilot/99999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Pilot not found"}

def test_create_pilot_missing_fields():
    pilot_data = {
        "ime": "Marko"
        # "priimek" nima vrednosti
    }

    response = client.post("/dodajPilota/", json=pilot_data)

    assert response.status_code == 422
    assert "detail" in response.json() 

def test_update_pilot_not_found():
    non_existent_id = 1234  
    updated_data = {"ime": "Johnny", "priimek": "DoeUpdated"}
    
    response = client.put(f"/pilot/{non_existent_id}", json=updated_data)
    
    assert response.status_code == 404
    assert response.json() == {"detail": "Pilot not found"}

