import sqlite3
import os
import pytest

def init_db(db_path):
    if not os.path.exists(os.path.dirname(db_path)):
        os.makedirs(os.path.dirname(db_path))

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create tables
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Letalo (
        idLetalo INTEGER PRIMARY KEY AUTOINCREMENT,
        ime_letala TEXT,
        tip TEXT,
        registrska_st TEXT UNIQUE,
        Polet_idPolet INTEGER
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Pilot (
        idPilot INTEGER PRIMARY KEY AUTOINCREMENT,
        ime TEXT,
        priimek TEXT
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Polet (
        idPolet INTEGER PRIMARY KEY AUTOINCREMENT,
        cas_vzleta INTEGER,
        cas_pristanka INTEGER,
        Pilot_idPilot INTEGER UNIQUE,
        FOREIGN KEY(Pilot_idPilot) REFERENCES Pilot(idPilot)
    )
    ''')

    # Insert initial data
    # cursor.execute("INSERT OR IGNORE INTO Pilot (ime, priimek) VALUES ('Janez', 'Novak')")
    # cursor.execute("INSERT OR IGNORE INTO Pilot (ime, priimek) VALUES ('Marko', 'Kranjc')")
    # cursor.execute("INSERT OR IGNORE INTO Letalo (ime_letala, tip, registrska_st) VALUES ('Orkan', 'Tovorno', 'SLO456')")
    # cursor.execute("INSERT OR IGNORE INTO Letalo (ime_letala, tip, registrska_st) VALUES ('Boeing 747', 'Commercial', 'SLO-456')")
    # conn.commit()

    # Yield the connection object for use in tests
    yield conn

    # Cleanup after test (e.g., closing the connection)
    conn.close()

def test_db():
    db_path = "app/tests/test.db"
    init_db(db_path)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    yield cursor, conn  
    conn.close()