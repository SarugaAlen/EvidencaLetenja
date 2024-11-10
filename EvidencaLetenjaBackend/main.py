import uvicorn as uvicorn
from fastapi import FastAPI, status, HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from pydantic import BaseModel
import sqlite3
from typing import List, Optional
from models.schemas import Letalo, Polet, Pilot
from core.database import initialize_database
from routes import letalo, pilot, polet

app = FastAPI()
povezava = "../database/polet_app_baza.db"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Add your frontend origin here
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

initialize_database()

app.include_router(polet.router)
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