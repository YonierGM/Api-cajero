from pydantic import BaseModel
from typing import Optional

class TipoTransaccion(BaseModel):
    tipotransaccionid: Optional[int]
    descripcion: str