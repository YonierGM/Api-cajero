from pydantic import BaseModel
from typing import Optional

class TipoCuenta(BaseModel):
    tipocuentaid: Optional[int]
    descripcion: str