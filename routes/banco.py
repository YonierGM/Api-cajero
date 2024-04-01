from fastapi import APIRouter, HTTPException, status
from typing import List
from sqlalchemy import insert, select, update, delete

from config.db import conn
from schemas.banco import Banco
from models.banco import bancos

bancosRoute = APIRouter()

@bancosRoute.get('/bancos', tags=['bancos'], response_model=List[Banco])
def get_bancos():
    return conn.execute(select(bancos)).fetchall()

@bancosRoute.get("/bancos/{id}", tags=["bancos"], response_model=Banco)
def get_banco(id: int):
    existing_banco = conn.execute(select(bancos).where(bancos.c.bancoid == id)).first()
    if existing_banco:
        return existing_banco
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Banco not found")

@bancosRoute.post("/bancos", tags=["bancos"], response_model=Banco)
def create_banco(banco: Banco):
    try:
        new_banco = {
            "numerobanco": banco.numerobanco,
            "nombre": banco.nombre,
            "cantcuentas": banco.cantcuentas,
            "montomaxtransaccion": banco.montomaxtransaccion,
            "montomintransaccion": banco.montomintransaccion,
            "cobroportransaccion": banco.cobroportransaccion,
            "interesporanio": banco.interesporanio,
        }
        result = conn.execute(insert(bancos).values(new_banco))
        new_banco["bancoid"] = result.inserted_primary_key[0]
        conn.commit()
        return new_banco
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@bancosRoute.put("/bancos/{id}", tags=["bancos"], response_model=Banco)
def update_banco(id: int, banco: Banco):
    existing_banco = conn.execute(select(bancos).where(bancos.c.bancoid == id)).fetchone()
    if existing_banco:
        conn.execute(
            update(bancos)
            .values(
                numerobanco=banco.numerobanco,
                nombre=banco.nombre,
                cantcuentas=banco.cantcuentas,
                montomaxtransaccion=banco.montomaxtransaccion,
                montomintransaccion=banco.montomintransaccion,
                cobroportransaccion=banco.cobroportransaccion,
                interesporanio=banco.interesporanio,
            )
            .where(bancos.c.bancoid == id)
        )
        conn.commit()
        banco_updated = conn.execute(select(bancos).where(bancos.c.bancoid == id)).fetchone()
        return banco_updated
    else:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Banco not found")

@bancosRoute.delete("/bancos/{id}", tags=["bancos"])
def delete_banco(id: int):
    existing_banco = conn.execute(select(bancos).where(bancos.c.bancoid == id)).fetchone()
    if existing_banco:
        if existing_banco.cantcuentas > 0:
            return "No se pude eliminar, el banco tiene cuentas activas"

        conn.execute(delete(bancos).where(bancos.c.bancoid == id))
        conn.commit()
        return status.HTTP_200_OK
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Banco not found")
