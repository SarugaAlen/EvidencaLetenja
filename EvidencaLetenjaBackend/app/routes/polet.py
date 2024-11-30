from fastapi import APIRouter, HTTPException
from core.database import get_connection
from models.schemas import Polet
from typing import List
from datetime import datetime

router = APIRouter()

@router.post("/dodajPolet/", response_model=Polet)
def create_polet(polet: Polet):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Polet (cas_vzleta, cas_pristanka, Pilot_idPilot) 
            VALUES (?, ?, ?)''', 
            (polet.cas_vzleta, polet.cas_pristanka, polet.Pilot_idPilot))
        conn.commit()
        polet.idPolet = cursor.lastrowid
    return polet

@router.get("/polet/{idPolet}", response_model=Polet)
def read_polet(idPolet: int):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Polet WHERE idPolet = ?", (idPolet,))
        row = cursor.fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Polet not found")

    return Polet(**dict(row)) 

@router.get("/pridobiPolete/", response_model=List[Polet])
def read_poleti():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Polet")
        rows = cursor.fetchall()
        return [Polet(**dict(row)) for row in rows]

@router.delete("/polet/{idPolet}", response_model=dict)
def delete_polet(idPolet: int):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Polet WHERE idPolet = ?", (idPolet,))
        conn.commit()
    return {"message": "Polet deleted successfully"}

@router.get("/pridobiPrihodnjeLete/", response_model=List[Polet])
def read_poleti_after_date():
    # Get the current date (resetting time to 00:00)
    current_date = datetime.now().date()

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT * FROM Polet 
            WHERE date(substr(cas_vzleta, 7, 4) || '-' || substr(cas_vzleta, 4, 2) || '-' || substr(cas_vzleta, 1, 2)) >= ?
            """,
            (current_date,)
        )

        poleti = cursor.fetchall()

    return [
        {
            "idPolet": row[0],
            "cas_vzleta": row[1],
            "cas_pristanka": row[2],
            "Pilot_idPilot": row[3]
        }
        for row in poleti
    ]

@router.get("/pridobiZgodovinoLetov/", response_model=List[Polet])
def read_poleti_before_date():
    # Get the current date (resetting time to 00:00)
    current_date = datetime.now().date()

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT * FROM Polet 
            WHERE date(substr(cas_vzleta, 7, 4) || '-' || substr(cas_vzleta, 4, 2) || '-' || substr(cas_vzleta, 1, 2)) < ?
            """,
            (current_date,)
        )

        poleti = cursor.fetchall()

    return [
        {
            "idPolet": row[0],
            "cas_vzleta": row[1],
            "cas_pristanka": row[2],
            "Pilot_idPilot": row[3]
        }
        for row in poleti
    ]

# Še potrebno spremeniti
@router.put("/poleti/{idPolet}", response_model=dict)
def update_polet(idPolet: int, polet: Polet):
    with get_connection() as conn:
        cursor = conn.cursor()

        # Fetch the existing flight details
        cursor.execute("SELECT * FROM Polet WHERE idPolet = ?", (idPolet,))
        existing_polet = cursor.fetchone()

        if not existing_polet:
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

    return {"message": f"Polet with id {idPolet} updated successfully"}