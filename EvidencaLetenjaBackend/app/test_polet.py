from fastapi.testclient import TestClient
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from main import app  

client = TestClient(app)

def test_create_polet():
    polet_data = {
        "cas_vzleta": "2024-11-30T08:00:00",
        "cas_pristanka": "2024-11-30T10:00:00",
        "Pilot_idPilot": 34562354
    }
    
    response = client.post("/dodajPolet/", json=polet_data)
    assert response.status_code == 200
    assert response.json()["cas_vzleta"] == polet_data["cas_vzleta"]
    assert response.json()["cas_pristanka"] == polet_data["cas_pristanka"]
    assert response.json()["Pilot_idPilot"] == polet_data["Pilot_idPilot"]


def test_read_poleti():
    response = client.get("/pridobiPolete/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_read_poleti_after_date():
    response = client.get("/pridobiPrihodnjeLete/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_delete_polet():
    polet_data = {
        "cas_vzleta": "2024-11-30T08:00:00",
        "cas_pristanka": "2024-11-30T10:00:00",
        "Pilot_idPilot": 2345346
    }

    create_response = client.post("/dodajPolet/", json=polet_data)
    created_polet_id = create_response.json()["idPolet"]

    response = client.delete(f"/polet/{created_polet_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Polet deleted successfully"}

    response = client.get(f"/polet/{created_polet_id}")
    assert response.status_code == 404 

