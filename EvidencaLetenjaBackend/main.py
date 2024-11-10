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
app.include_router(letalo.router)

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

@app.get("/", status_code=status.HTTP_200_OK)
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)