from fastapi.testclient import TestClient
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from main import app  

client = TestClient(app)


# 1. Test creating a new Letalo (POST /dodajLetalo/)
def test_create_letalo():
    letalo_data = {
        "ime_letala": "Airplane A",
        "tip": "Commercial",
        "registrska_st": "SLO1234",
        "Polet_idPolet": 1
    }

    # Send a POST request to create a new Letalo
    response = client.post("/dodajLetalo/", json=letalo_data)

    # Check if the response status code is 200 OK
    assert response.status_code == 200

    # Check if the response contains the expected data
    data = response.json()
    assert "idLetalo" in data
    assert data["ime_letala"] == letalo_data["ime_letala"]
    assert data["tip"] == letalo_data["tip"]
    assert data["registrska_st"] == letalo_data["registrska_st"]
    assert data["Polet_idPolet"] == letalo_data["Polet_idPolet"]

# 2. Test retrieving all Letalo objects (GET /pridobiLetala/)
def test_read_letalos():
    # Create a Letalo first to ensure there's at least one
    letalo_data = {
        "ime_letala": "Airplane B",
        "tip": "Cargo",
        "registrska_st": "SLO5678",
        "Polet_idPolet": 2
    }
    client.post("/dodajLetalo/", json=letalo_data)

    # Send a GET request to retrieve the list of Letalo
    response = client.get("/pridobiLetala/")

    # Check if the response status code is 200 OK
    assert response.status_code == 200

    # Check if the response contains a list of Letalo objects
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0  # Ensure there's at least one Letalo

    # Check if the created Letalo is in the response
    assert any(letalo["ime_letala"] == letalo_data["ime_letala"] for letalo in data)

# 3. Test deleting a Letalo (DELETE /letalo/{idLetalo})
def test_delete_letalo():
    # Create a Letalo to delete
    letalo_data = {
        "ime_letala": "Airplane C",
        "tip": "Private",
        "registrska_st": "SLO1111",
        "Polet_idPolet": 3
    }
    create_response = client.post("/dodajLetalo/", json=letalo_data)
    created_letalo_id = create_response.json()["idLetalo"]

    # Send a DELETE request to delete the Letalo
    response = client.delete(f"/letalo/{created_letalo_id}")

    # Check if the response status code is 200 OK
    assert response.status_code == 200
    assert response.json() == {"message": "Letalo deleted successfully"}

    # Send a GET request to check if the Letalo is deleted
    response = client.get(f"/letalo/{created_letalo_id}")
    assert response.status_code == 404  # The Letalo should no longer exist

# 4. Test updating a Letalo (PUT /letalo/{idLetalo})
def test_update_letalo():
    # First, create a Letalo to update
    letalo_data = {
        "ime_letala": "Airplane D",
        "tip": "Business",
        "registrska_st": "SLO8888",
        "Polet_idPolet": 4
    }
    create_response = client.post("/dodajLetalo/", json=letalo_data)
    created_letalo_id = create_response.json()["idLetalo"]

    # New data for the update
    updated_letalo_data = {
        "ime_letala": "Updated Airplane D",
        "tip": "Luxury",
        "registrska_st": "SLO9999",
        "Polet_idPolet": 5
    }

    # Send a PUT request to update the Letalo
    response = client.put(f"/letalo/{created_letalo_id}", json=updated_letalo_data)

    # Check if the response status code is 200 OK
    assert response.status_code == 200
    assert response.json() == {"message": f"Letalo with id {created_letalo_id} updated successfully"}

    # Send a GET request to verify the update
    response = client.get(f"/letalo/{created_letalo_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["ime_letala"] == updated_letalo_data["ime_letala"]
    assert data["tip"] == updated_letalo_data["tip"]
    assert data["registrska_st"] == updated_letalo_data["registrska_st"]
    assert data["Polet_idPolet"] == updated_letalo_data["Polet_idPolet"]