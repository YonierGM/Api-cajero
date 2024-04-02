from fastapi import APIRouter, HTTPException, status
from typing import List
from sqlalchemy import insert
from config.db import conn
from schemas.tipotransaccion import TipoTransaccion
from models.tipotransaccion import tipotransacciones

tipotransaccionRoute = APIRouter()

@tipotransaccionRoute.get('/tipotransacciones', tags=['tipotransacciones'], response_model=List[TipoTransaccion])
def get_tipotransacciones():
    return conn.execute(tipotransacciones.select()).fetchall()

@tipotransaccionRoute.get("/tipotransacciones/{id}", tags=["tipotransacciones"], response_model=TipoTransaccion)
def get_tipotransaccion(id: int):
    existing_tipotransaccion = conn.execute(tipotransacciones.select().where(tipotransacciones.c.tipotransaccionid == id)).first()
    if existing_tipotransaccion:
        return existing_tipotransaccion
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tipo de Transacción no encontrada")

@tipotransaccionRoute.post("/tipotransacciones", tags=["tipotransacciones"], response_model=TipoTransaccion)
def create_tipotransaccion(tipotransaccion: TipoTransaccion):
    try:
        new_tipotransaccion = {
            "descripcion": tipotransaccion.descripcion,
        }
        result = conn.execute(insert(tipotransacciones).values(new_tipotransaccion))
        new_tipotransaccion["tipotransaccionid"] = result.inserted_primary_key[0]
        conn.commit()
        return new_tipotransaccion
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@tipotransaccionRoute.put("/tipotransacciones/{id}", tags=["tipotransacciones"], response_model=TipoTransaccion)
def update_tipotransaccion(id: int, tipotransaccion: TipoTransaccion):
    existing_tipotransaccion = conn.execute(tipotransacciones.select().where(tipotransacciones.c.tipotransaccionid == id)).fetchone()
    if existing_tipotransaccion:
        conn.execute(
            tipotransacciones.update()
            .values(
                descripcion=tipotransaccion.descripcion,
            )
            .where(tipotransacciones.c.tipotransaccionid == id)
        )
        conn.commit()
        tipotransaccion_updated = conn.execute(tipotransacciones.select().where(tipotransacciones.c.tipotransaccionid == id)).fetchone()
        return tipotransaccion_updated
    else:
         return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tipo de Transacción no encontrada")

@tipotransaccionRoute.delete("/tipotransacciones/{id}", tags=["tipotransacciones"])
def delete_tipotransaccion(id: int):
    existing_tipotransaccion = conn.execute(tipotransacciones.select().where(tipotransacciones.c.tipotransaccionid == id)).fetchone()
    if existing_tipotransaccion:
        conn.execute(tipotransacciones.delete().where(tipotransacciones.c.tipotransaccionid == id))
        conn.commit()
        return status.HTTP_200_OK
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tipo de Transacción no encontrada")
