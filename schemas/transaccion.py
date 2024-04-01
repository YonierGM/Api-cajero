from pydantic import BaseModel

class Transaccion(BaseModel):
    montotransaccion: int
    cuentaid: int
    personaid: int
    tipotransaccionid: int