import sys
import os
import pytest
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from fastapi.testclient import TestClient
import sqlite3
from models.schemas import Polet
from app.main import app 

client = TestClient(app)


@pytest.fixture(scope="function")
def test_db():
    db_path = "app/tests/test.db"
    init_db(db_path)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    yield cursor, conn  
    conn.close()


def init_db(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    conn.close()


def test_read_polet(test_db):
    response = client.get("/pridobiPolete/")

    assert response.status_code == 200

    data = response.json()
    print(data)

    assert data[0]["cas_vzleta"] == "16/06/2023 08:00"
    assert data[0]["cas_pristanka"] == "16/06/2023 09:45"
    assert data[0]["Pilot_idPilot"] == 5

# def test_create_polet():
#     response = client.post("/dodajPolet/", json={"cas_vzleta": "2024-11-30T08:00:00", "cas_pristanka": "2024-11-30T08:00:00"})

#     assert response.status_code == 201

#     data = response.json()

#     assert data["cas_vzleta"] == "2024-11-30T08:00:00"
#     assert data["cas_pristanka"] == "2024-11-30T08:00:00"





