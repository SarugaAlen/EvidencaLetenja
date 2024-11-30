import sys
import os
import pytest
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from fastapi.testclient import TestClient
import sqlite3
from models.schemas import Pilot
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

def test_read_pilot(test_db):
    response = client.get("/pridobiPilote/")

    assert response.status_code == 200

    data = response.json()

    assert data[0]["ime"] == "Marko"
    assert data[0]["priimek"] == "Novak"

def test_create_pilot():
    response = client.post("/dodajPilota/", json={"ime": "Test", "priimek": "Test"})

    assert response.status_code == 200

    data = response.json()

    assert data["ime"] == "Test"
    assert data["priimek"] == "Test"


