import sys
import os
from fastapi.testclient import TestClient
from fastapi import FastAPI, status

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from main import app as app

client = TestClient(app)

def test_read_pilots():
    test_data = {
        "ime": "Alen",
        "priimek": "Test"
    }

    client.post("/dodajPilota/", json=test_data)

    response = client.get("/pridobiPilote/")

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0  

    assert any(pilot["ime"] == test_data["ime"] and pilot["priimek"] == test_data["priimek"] for pilot in data)

def test_create_pilot():
    response = client.post("/dodajPilota/", json={"ime": "Test", "priimek": "Test"})

    assert response.status_code == 200

    data = response.json()

    assert data["ime"] == "Test"
    assert data["priimek"] == "Test"

def test_update_pilot():
    test_data = {
        "ime": "Test",
        "priimek": "Test"
    }

    response = client.post("/dodajPilota/", json=test_data)
    id = response.json()["idPilot"]

    update_data = {
        "ime": "Test2",
        "priimek": "Test2"
    }

    response = client.put(f"/pilot/{id}", json=update_data)

    assert response.status_code == 200

    data = response.json()

    assert data["ime"] == "Test2"
    assert data["priimek"] == "Test2"

    response = client.get(f"/pilot/{id}")

    assert response.status_code == 200

    data = response.json()

    assert data["ime"] == "Test2"
    assert data["priimek"] == "Test2"

def test_delete_pilot():
    test_data = {
        "ime": "Test",
        "priimek": "Test"
    }

    response = client.post("/dodajPilota/", json=test_data)
    id = response.json()["idPilot"]

    response = client.delete(f"/pilot/{id}")

    assert response.status_code == 200
    assert response.json() == {"message": "Pilot deleted successfully"}

    response = client.get(f"/pilot/{id}")
    assert response.status_code == 404


def test_get_non_existent_pilot():
    response = client.get("/pilot/999999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Pilot not found"}


def test_create_pilot_missing_fields():
    test_data = {
        "ime": "Test"
    }

    response = client.post("/dodajPilota/", json=test_data)

    assert response.status_code == 422
    assert "detail" in response.json() 


def test_get_pilots_valid_number():
    stevilo = 3
    
    response = client.get(f"/pridobiPilote/{stevilo}")
    
    assert response.status_code == 200
    
    data = response.json()
    
    assert len(data) == stevilo

def test_get_pilots_invalid_number():
    stevilo = -5
    
    response = client.get(f"/pridobiPilote/{stevilo}")
    
    assert response.status_code == 400
    
    assert response.json() == {"detail": "The number of pilots must be greater than zero"}
