import os
import sqlite3

#DATABASE_URL = os.path.join(os.path.dirname(__file__), "../../../database/test.db")

DATABASE_URL = os.path.join(os.path.dirname(__file__), "../database/test.db")

os.makedirs(os.path.dirname(DATABASE_URL), exist_ok=True)

def get_connection():
    conn = sqlite3.connect(DATABASE_URL)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_database():
    with get_connection() as conn:
        cursor = conn.cursor()
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

        cursor.execute('''CREATE TABLE IF NOT EXISTS Certifikat (
            idCertifikat INTEGER PRIMARY KEY,
            idPilot INTEGER,
            ime_certifikata TEXT,
            datum_izdaje TEXT,
            datum_izteka TEXT
            )''')

        cursor.executemany('''INSERT INTO Pilot (ime, priimek) VALUES (?, ?)''', [
            ('Janez', 'Novak'),
            ('Miha', 'Kovac'),
            ('Andrej', 'Zajc'),
            ('Marko', 'Horvat'),
            ('Luka', 'Petrovic'),
            ('Nina', 'Simic'),
            ('Ana', 'Jovanovic'),
            ('Tina', 'Racic'),
            ('Ivan', 'Bencic'),
            ('Sasa', 'Breznik')
        ])

        # Insert data into Letalo table
        cursor.executemany('''INSERT INTO Letalo (ime_letala, tip, registrska_st, Polet_idPolet) VALUES (?, ?, ?, ?)''', [
            ('Letalo A123', 'Passenger', 'SLO123', 1),
            ('Letalo B456', 'Cargo', 'SLO456', 2),
            ('Letalo C789', 'Military', 'SLO789', 3),
            ('Letalo D012', 'Private', 'SLO012', 4),
            ('Letalo E345', 'Passenger', 'SLO345', 5),
            ('Letalo F678', 'Cargo', 'SLO678', 6),
            ('Letalo G901', 'Military', 'SLO901', 7),
            ('Letalo H234', 'Private', 'SLO234', 8),
            ('Letalo I567', 'Passenger', 'SLO567', 9),
            ('Letalo J890', 'Cargo', 'SLO890', 10)
        ])

        cursor.executemany('''INSERT INTO Polet (cas_vzleta, cas_pristanka, Pilot_idPilot) VALUES (?, ?, ?)''', [
            ('01/12/2024 08:00', '01/12/2024 10:00', 1),
            ('02/12/2024 09:30', '02/12/2024 11:30', 2),
            ('03/12/2024 10:00', '03/12/2024 12:00', 3),
            ('04/12/2024 12:15', '04/12/2024 14:15', 4),
            ('05/12/2024 14:30', '05/12/2024 16:30', 5),
            ('06/12/2024 07:00', '06/12/2024 09:00', 6),
            ('07/12/2024 08:15', '07/12/2024 10:15', 7),
            ('08/12/2024 13:00', '08/12/2024 15:00', 8),
            ('09/12/2024 11:45', '09/12/2024 13:45', 9),
            ('10/12/2024 15:30', '10/12/2024 17:30', 10)
        ])


        cursor.executemany('''
             INSERT INTO Certifikat (idCertifikat, idPilot, ime_certifikata, datum_izdaje, datum_izteka)
             VALUES (NULL, ?, ?, ?, ?)
         ''', [
             (1, 'Licenca komercialnega pilota', '2022-01-15', '2025-01-15'),
             (2, 'Licenca za inštruktorja letenja', '2023-02-12', '2026-02-12'),
             (3, 'Licenca za naprednega pilota', '2021-11-10', '2024-11-10'),
             (4, 'Licenca za prevoznika tovora', '2020-05-23', '2023-05-23'),
             (5, 'Licenca za pilota zračnega ladje', '2022-08-16', '2025-08-16'),
             (6, 'Licenca za letalskega inštruktorja', '2019-03-20', '2022-03-20'),
             (7, 'Licenca za pilota brezpilotnih letal', '2023-06-14', '2026-06-14'),
             (8, 'Licenca za prevoznika potnikov', '2021-09-09', '2024-09-09'),
             (9, 'Licenca za pilota civilnih letal', '2020-12-01', '2023-12-01'),
             (10, 'Licenca za pilota letalskih razgledov', '2018-07-14', '2021-07-14')
         ])
        
     

        conn.commit()

