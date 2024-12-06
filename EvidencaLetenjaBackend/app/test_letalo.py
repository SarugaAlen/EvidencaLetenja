import sys
import os
from fastapi.testclient import TestClient
from fastapi import FastAPI, status


sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from main import app as app

client = TestClient(app)


def test_read_letala():
    test_data = {
        "ime_letala": "Airplane TEST",
        "tip": "Testiramo",
        "registrska_st": "SLO765",
        "Polet_idPolet": 5
    }
     
    client.post("/dodajLetalo/", json=test_data)
    response = client.get("/pridobiLetala/")

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0 

    assert any(letalo["ime_letala"] == test_data["ime_letala"] for letalo in data)


def test_create_letalo():
    response = client.post("/dodajLetalo/", json={"ime_letala": "Test", "tip": "Testno", "registrska_st": "TEST123"})

    assert response.status_code == 201

    data = response.json()

    assert data["ime_letala"] == "Test"
    assert data["tip"] == "Testno"
    assert data["registrska_st"] == "TEST123"

def test_update_letalo():
    test_data = {
        "ime_letala": "Airplane TEST",
        "tip": "Testiramo",
        "registrska_st": "SLO765",
        "Polet_idPolet": 5
    }
    create_response = client.post("/dodajLetalo/", json=test_data)
    created_letalo_id = create_response.json()["idLetalo"]

    updated_letalo_data = {
        "ime_letala": "Updated Airplane D",
        "tip": "Luxury",
        "registrska_st": "SLO9999",
        "Polet_idPolet": 5
    }

    response = client.put(f"/letalo/{created_letalo_id}", json=updated_letalo_data)

    assert response.status_code == 200
    assert response.json() == {"message": f"Letalo with id {created_letalo_id} updated successfully"}

    response = client.get(f"/letalo/{created_letalo_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["ime_letala"] == updated_letalo_data["ime_letala"]
    assert data["tip"] == updated_letalo_data["tip"]
    assert data["registrska_st"] == updated_letalo_data["registrska_st"]
    assert data["Polet_idPolet"] == updated_letalo_data["Polet_idPolet"]


