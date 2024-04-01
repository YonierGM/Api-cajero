from pydantic import BaseModel
from datetime import date
from typing import Optional

class Cuenta(BaseModel):
    cuentaid: Optional[int]
    bancoid: int
    personaid: int
    tipocuentaid: int
    numerocuenta: int
    saldocuenta: int
    fechacreacion: date