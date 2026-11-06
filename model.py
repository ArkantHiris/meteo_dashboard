from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator


class VilleModel(BaseModel):

    id: Optional[int] = None
    nom: str = Field(..., min_length=1)
    latitude: float = Field(..., ge=-90.0, le=90.0)
    longitude: float = Field(..., ge=-180.0, le=180.0)


class ReleveModel(BaseModel):

    id: Optional[int] = None
    ville_id: int
    temperature: float
    vitesse_vent: float = Field(..., ge=0.0)
    date_heure: datetime

    # method si la date reçue n'a pas le bon format
    @field_validator('date_heure', mode='before')
    @classmethod
    def parse_date(cls, value):
        if isinstance(value, str):
            return datetime.fromisoformat(value)
        return value

