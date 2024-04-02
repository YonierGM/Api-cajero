from pydantic import BaseModel
from datetime import date
from typing import Optional

class Transaccion(BaseModel):

    transaccionid: Optional[int]
    montotransaccion: int
    cuentaid: int
    fechatransaccion: date
    personaid: int
    tipotransaccionid: int