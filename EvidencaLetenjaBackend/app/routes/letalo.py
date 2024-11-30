from fastapi import APIRouter, HTTPException
from core.database import get_connection
from models.schemas import Letalo
from typing import List

router = APIRouter()

@router.post("/dodajLetalo/", response_model=Letalo)
def create_letalo(letalo: Letalo):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Letalo (ime_letala, tip, registrska_st, Polet_idPolet) 
            VALUES (?, ?, ?, ?)''', 
            (letalo.ime_letala, letalo.tip, letalo.registrska_st, letalo.Polet_idPolet))
        conn.commit()
        letalo.idLetalo = cursor.lastrowid
    return letalo

@router.get("/pridobiLetala/", response_model=List[Letalo])
def read_letalos():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Letalo")
        rows = cursor.fetchall()
        return [Letalo(**dict(row)) for row in rows]

@router.delete("/letalo/{idLetalo}", response_model=dict)
def delete_letalo(idLetalo: int):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Letalo WHERE idLetalo = ?", (idLetalo,))
        conn.commit()
    return {"message": "Letalo deleted successfully"}

@router.put("/letalo/{idLetalo}", response_model=dict)
def update_letalo(idLetalo: int, letalo: Letalo):
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Letalo WHERE idLetalo = ?", (idLetalo,))
        existing_letalo = cursor.fetchone()
        
        if not existing_letalo:
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

    return {"message": f"Letalo with id {idLetalo} updated successfully"}


@router.get("/letalo/{idLetalo}", response_model=Letalo)
def get_letalo_by_id(idLetalo: int):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Letalo WHERE idLetalo = ?", (idLetalo,))
        row = cursor.fetchone()

        if row is None:
            raise HTTPException(status_code=404, detail="Letalo not found")

        return Letalo(**dict(row))
