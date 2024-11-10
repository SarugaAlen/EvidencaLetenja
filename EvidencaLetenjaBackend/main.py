import uvicorn as uvicorn
from fastapi import FastAPI, status, HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from pydantic import BaseModel
import sqlite3
from typing import List, Optional
from models.schemas import Letalo, Polet, Pilot

app = FastAPI()
povezava = "../database/polet_app_baza.db"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Add your frontend origin here
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

### API poleti

# Delujoče
@app.post("/dodajPolet/", response_model=Polet)
def create_polet(polet: Polet):
    conn = sqlite3.connect(povezava)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Polet WHERE Pilot_idPilot = ?", (polet.Pilot_idPilot,))
    existing_polet = cursor.fetchone()
    if existing_polet:
        conn.close()
        return {**polet.dict(), "idPolet": existing_polet[0]}

    cursor.execute('''
    INSERT INTO Polet (cas_vzleta, cas_pristanka, Pilot_idPilot)
    VALUES (?, ?, ?)
    ''', (polet.cas_vzleta, polet.cas_pristanka, polet.Pilot_idPilot))
    conn.commit()
    polet_id = cursor.lastrowid
    conn.close()
    
    return {**polet.dict(), "idPolet": polet_id}

#Delujoče
@app.get("/pridobiPolete/", response_model=List[Polet])
def read_poleti():
    conn = sqlite3.connect(povezava)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Polet")
    poleti = cursor.fetchall()
    conn.close()
    return [{"idPolet": row[0], "cas_vzleta": row[1], "cas_pristanka": row[2], "Pilot_idPilot": row[3]} for row in poleti]

@app.get("/pridobiPrihodnjeLete/", response_model=List[Polet])
def read_poleti_after_date():
    # Get the current date (resetting time to 00:00)
    current_date = datetime.now().date()

    # Connect to the database and query for flights after the current date
    conn = sqlite3.connect(povezava)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT * FROM Polet 
        WHERE date(substr(cas_vzleta, 7, 4) || '-' || substr(cas_vzleta, 4, 2) || '-' || substr(cas_vzleta, 1, 2)) >= ?
        """,
        (current_date,)
    )

    poleti = cursor.fetchall()
    conn.close()

    return [
        {
            "idPolet": row[0],
            "cas_vzleta": row[1],
            "cas_pristanka": row[2],
            "Pilot_idPilot": row[3]
        }
        for row in poleti
    ]

@app.get("/pridobiZgodovinoLetov/", response_model=List[Polet])
def read_poleti_before_date():
    current_date = datetime.now().date()

    conn = sqlite3.connect(povezava)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT * FROM Polet 
        WHERE date(substr(cas_vzleta, 7, 4) || '-' || substr(cas_vzleta, 4, 2) || '-' || substr(cas_vzleta, 1, 2)) < ?
        """,
        (current_date,)
    )

    poleti = cursor.fetchall()
    conn.close()

    return [
        {
            "idPolet": row[0],
            "cas_vzleta": row[1],
            "cas_pristanka": row[2],
            "Pilot_idPilot": row[3]
        }
        for row in poleti
    ]

#Delujoče
@app.delete("/polet/{idPolet}", response_model=dict)
def delete_polet(idPolet: int):
    conn = sqlite3.connect(povezava)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Polet WHERE idPolet = ?", (idPolet,))
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Polet not found")
    conn.commit()
    conn.close()
    
    return {"message": f"Polet with id {idPolet} deleted successfully"}


# Še potrebno spremeniti
@app.put("/poleti/{idPolet}", response_model=dict)
def update_polet(idPolet: int, polet: Polet):
    conn = sqlite3.connect(povezava)
    cursor = conn.cursor()

    # Fetch the existing flight details
    cursor.execute("SELECT * FROM Polet WHERE idPolet = ?", (idPolet,))
    existing_polet = cursor.fetchone()

    if not existing_polet:
        conn.close()
        raise HTTPException(status_code=404, detail="Polet not found")

    # Initialize a list to hold the update parameters
    update_fields = []
    update_values = []

    # Check and append the new values for `cas_vzleta` and `cas_pristanka`
    if polet.cas_vzleta is not None:
        update_fields.append("cas_vzleta = ?")
        update_values.append(polet.cas_vzleta)

    if polet.cas_pristanka is not None:
        update_fields.append("cas_pristanka = ?")
        update_values.append(polet.cas_pristanka)

    # Only proceed if there are fields to update
    if update_fields:
        # Create the SQL statement dynamically
        sql_update_query = f'''
            UPDATE Polet
            SET {', '.join(update_fields)}
            WHERE idPolet = ?
        '''
        update_values.append(idPolet)
        cursor.execute(sql_update_query, update_values)
        conn.commit()

    conn.close()

    return {"message": f"Polet with id {idPolet} updated successfully"}

### API Letalo
#Delujoče
@app.delete("/letalo/{idLetalo}", response_model=dict)
def delete_letalo(idLetalo: int):
    conn = sqlite3.connect(povezava)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Letalo WHERE idLetalo = ?", (idLetalo,))
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Letalo not found")
    conn.commit()
    conn.close()
    
    return {"message": f"Letalo with id {idLetalo} deleted successfully"}

### API Pilot

#Delujoče
@app.delete("/pilot/{idPilot}", response_model=dict)
def delete_pilot(idPilot: int):
    conn = sqlite3.connect(povezava)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Pilot WHERE idPilot = ?", (idPilot,))
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Pilot not found")
    conn.commit()
    conn.close()
    
    return {"message": f"Pilot with id {idPilot} deleted successfully"}

## Delujoče
@app.post("/dodajLetalo/")
def create_letalo(letalo: Letalo):
    conn = sqlite3.connect(povezava)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Letalo WHERE registrska_st = ?", (letalo.registrska_st,))
    existing_letalo = cursor.fetchone()
    if existing_letalo:
        conn.close()
        return {**letalo.dict(), "idLetalo": existing_letalo[0]}

    cursor.execute('''
    INSERT INTO Letalo (ime_letala, tip, registrska_st, Polet_idPolet)
    VALUES (?, ?, ?, ?)
    ''', (letalo.ime_letala, letalo.tip, letalo.registrska_st, letalo.Polet_idPolet))
    conn.commit()
    letalo_id = cursor.lastrowid
    conn.close()
    
    return {**letalo.dict(), "idLetalo": letalo_id}

#Delujoče
@app.get("/pridobiLetala/", response_model=List[Letalo])
def read_letalos():
    conn = sqlite3.connect(povezava)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Letalo")
    letalos = cursor.fetchall()
    conn.close()
    
    return [{"idLetalo": row[0], "ime_letala": row[1], "tip": row[2], "registrska_st": row[3], "Polet_idPolet": row[4]} for row in letalos]


#Delujoče
@app.post("/dodajPilota/", response_model=Pilot)
def create_pilot(pilot: Pilot):
    conn = sqlite3.connect(povezava)
    cursor = conn.cursor()

    # Check if a pilot with the same name exists
    cursor.execute("SELECT * FROM Pilot WHERE ime = ? AND priimek = ?", (pilot.ime, pilot.priimek))
    existing_pilot = cursor.fetchone()
    if existing_pilot:
        conn.close()
        return {**pilot.dict(), "idPilot": existing_pilot[0]}

    cursor.execute('''
    INSERT INTO Pilot (ime, priimek)
    VALUES (?, ?)
    ''', (pilot.ime, pilot.priimek))
    conn.commit()
    pilot_id = cursor.lastrowid
    conn.close()
    
    return {**pilot.dict(), "idPilot": pilot_id}

#Delujoče
@app.get("/pridobiPilote/", response_model=List[Pilot])
def read_pilots():
    conn = sqlite3.connect(povezava)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Pilot")
    pilots = cursor.fetchall()
    conn.close()
    
    return [{"idPilot": row[0], "ime": row[1], "priimek": row[2]} for row in pilots]

#Delujoče
@app.put("/letalo/{idLetalo}", response_model=dict)
def update_letalo(idLetalo: int, letalo: Letalo):
    conn = sqlite3.connect(povezava)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Letalo WHERE idLetalo = ?", (idLetalo,))
    existing_letalo = cursor.fetchone()
    if not existing_letalo:
        conn.close()
        raise HTTPException(status_code=404, detail="Letalo not found")

    update_fields = {
        "ime_letala": letalo.ime_letala or existing_letalo[1],
        "tip": letalo.tip or existing_letalo[2],
        "registrska_st": letalo.registrska_st or existing_letalo[3],
        "Polet_idPolet": letalo.Polet_idPolet if letalo.Polet_idPolet is not None else existing_letalo[4]
    }

    cursor.execute(
        '''
        UPDATE Letalo
        SET ime_letala = ?, tip = ?, registrska_st = ?, Polet_idPolet = ?
        WHERE idLetalo = ?
        ''',
        (update_fields["ime_letala"], update_fields["tip"], update_fields["registrska_st"], update_fields["Polet_idPolet"], idLetalo)
    )
    conn.commit()
    conn.close()

    return {"message": f"Letalo with id {idLetalo} updated successfully"}

@app.get("/", status_code=status.HTTP_200_OK)
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)