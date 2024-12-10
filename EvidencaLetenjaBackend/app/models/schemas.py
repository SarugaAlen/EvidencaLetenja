from pydantic import BaseModel
from typing import Optional, List

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
    cas_vzleta: str  # Stored as text
    cas_pristanka: str  # Stored as text
    Pilot_idPilot: Optional[int]

class Certifikat(BaseModel):
    idCertifikat: Optional[int] = None
    idPilot: int
    ime_certifikata: str
    datum_izdaje: str  # Format: YYYY-MM-DD
    datum_izteka: str  # Format: YYYY-MM-DD