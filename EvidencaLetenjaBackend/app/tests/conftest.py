import pytest
import sqlite3
from app.tests.testna_baza_setup import init_db
import os

@pytest.fixture(scope="function")
def test_db():
    db_path = os.path.join(os.path.dirname(__file__), 'test.db')
    
    init_db(db_path)
    
    conn = sqlite3.connect(db_path)
    
    yield conn
    
    conn.close()
