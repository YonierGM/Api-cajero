from fastapi import APIRouter, HTTPException, status
from typing import List
from sqlalchemy import insert, select, update, delete

from config.db import conn
from schemas.tipocuenta import TipoCuenta
from models.tipocuenta import tipocuentas

tipocuentasRoute = APIRouter()

@tipocuentasRoute.get('/tipocuentas', tags=['tipocuentas'], response_model=List[TipoCuenta])
def get_tipocuentas():
    return conn.execute(select(tipocuentas)).fetchall()

@tipocuentasRoute.get("/tipocuentas/{id}", tags=["tipocuentas"], response_model=TipoCuenta)
def get_tipocuenta(id: int):
    existing_tipocuenta = conn.execute(select(tipocuentas).where(tipocuentas.c.tipocuentaid == id)).first()
    if existing_tipocuenta:
        return existing_tipocuenta
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tipo de cuenta not found")

@tipocuentasRoute.post("/tipocuentas", tags=["tipocuentas"], response_model=TipoCuenta)
def create_tipocuenta(tipocuenta: TipoCuenta):
    try:
        new_tipocuenta = {
            "descripcion": tipocuenta.descripcion
        }
        result = conn.execute(insert(tipocuentas).values(new_tipocuenta))
        new_tipocuenta["tipocuentaid"] = result.inserted_primary_key[0]
        conn.commit()
        return new_tipocuenta
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@tipocuentasRoute.put("/tipocuentas/{id}", tags=["tipocuentas"], response_model=TipoCuenta)
def update_tipocuenta(id: int, tipocuenta: TipoCuenta):
    existing_tipocuenta = conn.execute(select(tipocuentas).where(tipocuentas.c.tipocuentaid == id)).fetchone()
    if existing_tipocuenta:
        conn.execute(
            update(tipocuentas)
            .values(
                descripcion=tipocuenta.descripcion,
            )
            .where(tipocuentas.c.tipocuentaid == id)
        )
        conn.commit()
        tipocuenta_updated = conn.execute(select(tipocuentas).where(tipocuentas.c.tipocuentaid == id)).fetchone()
        return tipocuenta_updated
    else:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tipo de cuenta not found")

@tipocuentasRoute.delete("/tipocuentas/{id}", tags=["tipocuentas"])
def delete_tipocuenta(id: int):
    existing_tipocuenta = conn.execute(select(tipocuentas).where(tipocuentas.c.tipocuentaid == id)).fetchone()
    if existing_tipocuenta:
        conn.execute(delete(tipocuentas).where(tipocuentas.c.tipocuentaid == id))
        conn.commit()
        return status.HTTP_200_OK
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tipo de cuenta not found")
