from fastapi import APIRouter, HTTPException
from core.database import get_connection
from models.schemas import Pilot, Certifikat
from typing import List

router = APIRouter()

# Create Certification
@router.post("/dodajCertifikat/", response_model=Certifikat)
def create_certifikat(certifikat: Certifikat):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Certifikat (idPilot, ime_certifikata, datum_izdaje, datum_izteka)
            VALUES (?, ?, ?, ?)''', 
            (certifikat.idPilot, certifikat.ime_certifikata, certifikat.datum_izdaje, certifikat.datum_izteka))
        conn.commit()
        certifikat.idCertifikat = cursor.lastrowid  # Get the last inserted ID
    return certifikat

# Get Certifications by Pilot
@router.get("/certifikatiPilota/{idPilot}", response_model=List[Certifikat])
def get_certifications_by_pilot(idPilot: int):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Certifikat WHERE idPilot = ?", (idPilot,))
        rows = cursor.fetchall()
        return [Certifikat(**dict(row)) for row in rows] if rows else []

# Delete Certification
@router.delete("/certifikat/{idCertifikat}", response_model=dict)
def delete_certification(idCertifikat: int):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Certifikat WHERE idCertifikat = ?", (idCertifikat,))
        conn.commit()

        if cursor.rowcount == 0:  # No rows were deleted
            raise HTTPException(status_code=404, detail="Certifikat ni bil najden")  # Return error if not found

    return {"message": "Certifikat uspešno izbrisan"}

# Update Certification
@router.put("/certifikat/{idCertifikat}", response_model=Certifikat)
def update_certification(idCertifikat: int, certification: Certifikat):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE Certifikat
            SET ime_certifikata = ?, datum_izdaje = ?, datum_izteka = ?
            WHERE idCertifikat = ?''',
            (certification.ime_certifikata, certification.datum_izdaje, certification.datum_izteka, idCertifikat))
        conn.commit()

        if cursor.rowcount == 0:  # No rows were updated
            raise HTTPException(status_code=404, detail="Certifikat ni bil najden")  # Return error if not found

        certification.idCertifikat = idCertifikat  # Set the updated id
    return certification
