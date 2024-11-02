import uvicorn as uvicorn
from fastapi import FastAPI, status, HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from pydantic import BaseModel
import sqlite3
from typing import List, Optional

app = FastAPI()
povezava = "../database/polet_app_baza.db"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Add your frontend origin here
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

### Modeli
class Letalo(BaseModel):
    idLetalo: Optional[int] = None
    ime_letala: Optional[str] = None
    tip: Optional[str] = None
    registrska_st: Optional[str] = None
    Polet_idPolet: Optional[int] = None

class Pilot(BaseModel):
    idPilot: Optional[int] = None
    ime: str
    priimek: str

class Polet(BaseModel):
    idPolet: Optional[int] = None
    cas_vzleta: int
    cas_pristanka: int
    Pilot_idPilot: int

### API poleti
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

@app.get("/pridobiPolet/", response_model=List[Polet])
def read_poleti():
    conn = sqlite3.connect(povezava)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Polet")
    poleti = cursor.fetchall()
    conn.close()
    return [{"idPolet": row[0], "cas_vzleta": row[1], "cas_pristanka": row[2], "Pilot_idPilot": row[3]} for row in poleti]

### Potrebno testiranje
@app.get("/pridobiPoletPredDatumom/", response_model=List[Polet])
def read_poleti_before_date(date: str = Query(..., description="Date in format YYYY-MM-DD")):
    try:
        formatted_date = datetime.strptime(date, "%Y-%m-%d").strftime("%d%m%Y%H%M")  # Adjust as needed
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Please use YYYY-MM-DD.")

    conn = sqlite3.connect(povezava)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM Polet WHERE cas_vzleta < ?", (formatted_date,))
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

@app.put("/poleti/{idPolet}", response_model=dict)
def update_polet(idPolet: int, polet: Polet):
    conn = sqlite3.connect(povezava)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Polet WHERE idPolet = ?", (idPolet,))
    existing_polet = cursor.fetchone()
    if not existing_polet:
        conn.close()
        raise HTTPException(status_code=404, detail="Polet not found")

    update_fields = {
        "cas_vzleta": polet.cas_vzleta if polet.cas_vzleta is not None else existing_polet[1],
        "cas_pristanka": polet.cas_pristanka if polet.cas_pristanka is not None else existing_polet[2],
        "Pilot_idPilot": polet.Pilot_idPilot if polet.Pilot_idPilot is not None else existing_polet[3]
    }

    cursor.execute(
        '''
        UPDATE Polet
        SET cas_vzleta = ?, cas_pristanka = ?, Pilot_idPilot = ?
        WHERE idPolet = ?
        ''',
        (update_fields["cas_vzleta"], update_fields["cas_pristanka"], update_fields["Pilot_idPilot"], idPolet)
    )
    conn.commit()
    conn.close()

    return {"message": f"Polet with id {idPolet} updated successfully"}

### API Letalo
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

@app.post("/dodajLetalo/", response_model=Letalo)
def create_letalo(letalo: Letalo):
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()

    # Check if registrska_st already exists
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

@app.get("/pridobiLetala/", response_model=List[Letalo])
def read_letalos():
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Letalo")
    letalos = cursor.fetchall()
    conn.close()
    
    return [{"idLetalo": row[0], "ime_letala": row[1], "tip": row[2], "registrska_st": row[3], "Polet_idPolet": row[4]} for row in letalos]

# CRUD for Pilot
@app.post("/dodajPilota/", response_model=Pilot)
def create_pilot(pilot: Pilot):
    conn = sqlite3.connect("test.db")
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

@app.get("/pridobiPilote/", response_model=List[Pilot])
def read_pilots():
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Pilot")
    pilots = cursor.fetchall()
    conn.close()
    
    return [{"idPilot": row[0], "ime": row[1], "priimek": row[2]} for row in pilots]

@app.put("/letalo/{idLetalo}", response_model=dict)
def update_letalo(idLetalo: int, letalo: Letalo):
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()

    # Retrieve the existing Letalo to check if it exists
    cursor.execute("SELECT * FROM Letalo WHERE idLetalo = ?", (idLetalo,))
    existing_letalo = cursor.fetchone()
    if not existing_letalo:
        conn.close()
        raise HTTPException(status_code=404, detail="Letalo not found")

    # Prepare the update fields
    update_fields = {
        "ime_letala": letalo.ime_letala or existing_letalo[1],
        "tip": letalo.tip or existing_letalo[2],
        "registrska_st": letalo.registrska_st or existing_letalo[3],
        "Polet_idPolet": letalo.Polet_idPolet if letalo.Polet_idPolet is not None else existing_letalo[4]
    }

    # Execute the update in the database
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

@app.get("/hello/{name}")
async def say_hello(name: str):
    if name:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": f"Hello {name}"}
        )
    else:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": "Name is required"}
        )

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)