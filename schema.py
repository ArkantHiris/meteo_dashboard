# schemas.py
from datetime import datetime
from pydantic import BaseModel, Field, field_validator
from model import VilleModel

class VilleRead(VilleModel):
    id: int

    class Config:
        from_attributes = True

class VilleCreate(BaseModel):
    nom: str = Field(..., min_length=1)
    latitude: float = Field(..., ge=-90.0, le=90.0)
    longitude: float = Field(..., ge=-180.0, le=180.0)

class ReleveRead(BaseModel):
    id: int
    ville_id: int
    ville_nom: str  
    temperature: float
    vitesse_vent: float = Field(..., ge=0.0)
    date_heure: datetime

    @field_validator('date_heure', mode='before')
    @classmethod
    def parse_date(cls, value):
        if isinstance(value, str):
            return datetime.fromisoformat(value)
        return value