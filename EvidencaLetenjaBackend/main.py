import uvicorn as uvicorn
from fastapi import FastAPI, status, HTTPException, Query
from fastapi.responses import JSONResponse
from datetime import datetime
from pydantic import BaseModel
import sqlite3
from typing import List, Optional


app = FastAPI()
povezava = "../database/polet_app_baza.db"


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
        timestamp = int(datetime.strptime(date, "%Y-%m-%d").timestamp())
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Please use YYYY-MM-DD.")

    conn = sqlite3.connect(povezava)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Polet WHERE cas_vzleta < ?", (timestamp,))
    poleti = cursor.fetchall()
    conn.close()

    return [{"idPolet": row[0], "cas_vzleta": row[1], "cas_pristanka": row[2], "Pilot_idPilot": row[3]} for row in
            poleti]

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