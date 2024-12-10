from fastapi.testclient import TestClient
from fastapi import FastAPI, status
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from main import app  

client = TestClient(app)

def test_delete_non_existent_certification():
    non_existent_cert_id = 99999

    response = client.delete(f"/certifikat/{non_existent_cert_id}")
    assert response.status_code == 404

    assert response.json() == {"detail": "Not Found"}


# Test for getting a non-existent certification
def test_get_non_existent_certification():
    response = client.get("/certifikat/99999")
    
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}
