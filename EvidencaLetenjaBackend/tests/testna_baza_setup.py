import sqlite3

def init_db():
    conn = sqlite3.connect("test.db")
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

    cursor.execute("SELECT COUNT(*) FROM Letalo")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO Letalo (ime_letala, tip, registrska_st) VALUES (?, ?, ?)",
                       ("Airbus A320", "Commercial", "SLO-123"))
        cursor.execute("INSERT INTO Letalo (ime_letala, tip, registrska_st) VALUES (?, ?, ?)",
                       ("Boeing 747", "Commercial", "SLO-456"))

    cursor.execute("SELECT COUNT(*) FROM Pilot")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO Pilot (ime, priimek) VALUES (?, ?)", ("Janez", "Novak"))
        cursor.execute("INSERT INTO Pilot (ime, priimek) VALUES (?, ?)", ("Marko", "Kranjc"))

    cursor.execute("SELECT COUNT(*) FROM Polet")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO Polet (cas_vzleta, cas_pristanka, Pilot_idPilot) VALUES (?, ?, ?)",
                       (1609459200, 1609462800, 1))

    conn.commit()
    conn.close()

init_db()
