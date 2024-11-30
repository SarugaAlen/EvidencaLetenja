import sys
import os
import pytest
import sqlite3
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from fastapi.testclient import TestClient
from models.schemas import Letalo
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


def test_read_letala():
    response = client.get("/pridobiLetala/")

    assert response.status_code == 200

    data = response.json()

    assert data[0]["ime_letala"] == "Orkan"
    assert data[0]["tip"] == "Tovorno"
    assert data[0]["registrska_st"] == "SLO456"


def test_create_letalo():
    response = client.post("/dodajLetalo/", json={"ime_letala": "Test", "tip": "Testno", "registrska_st": "TEST123"})

    assert response.status_code == 201

    data = response.json()

    assert data["ime_letala"] == "Test"
    assert data["tip"] == "Testno"
    assert data["registrska_st"] == "TEST123"

def test_update_letalo():
    response = client.put("/letalo/32", json={"ime_letala": "Test", "tip": "Testno", "registrska_st": "TEST1234"})

    assert response.status_code == 200

    data = response.json()

    assert data["ime_letala"] == "Test"
    assert data["tip"] == "Testno"
    assert data["registrska_st"] == "TEST1234"


