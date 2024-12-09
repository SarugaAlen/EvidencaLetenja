from fastapi.testclient import TestClient
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from main import app  

client = TestClient(app)

def test_create_letalo():
    letalo_data = {
        "ime_letala": "Airplane A",
        "tip": "Commercial",
        "registrska_st": "SLO1234",
        "Polet_idPolet": 1
    }

    response = client.post("/dodajLetalo/", json=letalo_data)

    assert response.status_code == 200

    data = response.json()
    assert "idLetalo" in data
    assert data["ime_letala"] == letalo_data["ime_letala"]
    assert data["tip"] == letalo_data["tip"]
    assert data["registrska_st"] == letalo_data["registrska_st"]
    assert data["Polet_idPolet"] == letalo_data["Polet_idPolet"]

def test_read_letalos():
    letalo_data = {
        "ime_letala": "Airplane B",
        "tip": "Cargo",
        "registrska_st": "SLO5678",
        "Polet_idPolet": 2
    }

    client.post("/dodajLetalo/", json=letalo_data)

    response = client.get("/pridobiLetala/")

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0 

    assert any(letalo["ime_letala"] == letalo_data["ime_letala"] for letalo in data)

def test_delete_letalo():
    letalo_data = {
        "ime_letala": "Airplane C",
        "tip": "Private",
        "registrska_st": "SLO1111",
        "Polet_idPolet": 3
    }
    create_response = client.post("/dodajLetalo/", json=letalo_data)
    created_letalo_id = create_response.json()["idLetalo"]

    response = client.delete(f"/letalo/{created_letalo_id}")

    assert response.status_code == 200
    assert response.json() == {"message": "Letalo deleted successfully"}

    response = client.get(f"/letalo/{created_letalo_id}")
    assert response.status_code == 404  

def test_update_letalo():
    letalo_data = {
        "ime_letala": "Airplane D",
        "tip": "Business",
        "registrska_st": "SLO8888",
        "Polet_idPolet": 4
    }
    create_response = client.post("/dodajLetalo/", json=letalo_data)
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

def test_get_non_existing_letalo():
    non_existing_id = 9999 
    
    response = client.get(f"/letalo/{non_existing_id}")

    assert response.status_code == 404
    
    data = response.json()
    assert data["detail"] == "Letalo not found"

###Test