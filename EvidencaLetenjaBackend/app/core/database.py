import sqlite3

DATABASE_URL = "../database/test.db"

def get_connection():
    conn = sqlite3.connect(DATABASE_URL)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_database():
    with get_connection() as conn:
        cursor = conn.cursor()
        # Create the tables if they don't already exist
        cursor.execute('''CREATE TABLE IF NOT EXISTS Letalo (
            idLetalo INTEGER PRIMARY KEY,
            ime_letala TEXT,
            tip TEXT,
            registrska_st TEXT,
            Polet_idPolet INTEGER
        )''')
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS Pilot (
            idPilot INTEGER PRIMARY KEY,
            ime TEXT,
            priimek TEXT
        )''')
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS Polet (
            idPolet INTEGER PRIMARY KEY,
            cas_vzleta TEXT,
            cas_pristanka TEXT,
            Pilot_idPilot INTEGER
        )''')

        conn.commit()

