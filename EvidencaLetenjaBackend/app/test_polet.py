import sys
import os
import pytest
from fastapi.testclient import TestClient
import sqlite3
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import app as app

client = TestClient(app)

def test_read_poleti():
    response = client.get("/pridobiPolete/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_read_poleti_after_date():
    response = client.get("/pridobiPrihodnjeLete/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)






