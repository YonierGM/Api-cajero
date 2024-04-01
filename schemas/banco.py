from pydantic import BaseModel
from typing import Optional

class Banco(BaseModel):
    bancoid: Optional[int]
    numerobanco: int
    nombre: str
    cantcuentas: int
    montomaxtransaccion: int
    montomintransaccion: int
    cobroportransaccion: int
    interesporanio: int