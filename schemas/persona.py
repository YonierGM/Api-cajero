from pydantic import BaseModel
from typing import Optional
class Persona(BaseModel):
    personaid: Optional[int]
    nombre: str
    apellido: str
    cedula: int
    profesion: str