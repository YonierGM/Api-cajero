from fastapi import APIRouter, HTTPException, status

from sqlalchemy import insert, select, update, delete
from datetime import datetime

from config.db import conn

from models.cuenta import cuentas
from models.banco import bancos
from models.transaccion import transacciones
from schemas.transaccion import Transaccion


transaccionRoute = APIRouter()

@transaccionRoute.post("/deposito", tags=["transacciones"], status_code=status.HTTP_200_OK)
def hacer_deposito(transaccion: Transaccion):
    # Verificar si la cuenta existe y pertenece al banco
    cuenta = conn.execute(select(cuentas).where(cuentas.c.cuentaid == transaccion.cuentaid)).first()
    if not cuenta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cuenta not found")

    # Verificar si la cuenta está a nombre de la persona que hace la transacción
    if cuenta.personaid != transaccion.personaid:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No estas autorizado")

    # Verificar si la fecha de la transacción es posterior a la fecha de creación de la cuenta
    if transaccion.fechatransaccion < cuenta.fechacreacion:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La fecha de la transacción debe ser posterior a la fecha de creación de la cuenta.")

    #Obtengo el banco para capturar los montos por banco
    banco = conn.execute(select(bancos).where(bancos.c.bancoid == cuenta.bancoid)).first()

    # Verificar si el monto del depósito minimo es válido
    if transaccion.montotransaccion < banco.montomintransaccion:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El monto del depósito debe ser mayor o igual a: "+ str(banco.montomintransaccion))

    # Verificar si el monto del depósito maximo es válido
    if transaccion.montotransaccion > banco.montomaxtransaccion:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El monto del depósito debe ser menor o igual a: "+ str(banco.montomaxtransaccion))

    # Realizar el depósito
    nuevo_saldo = cuenta.saldocuenta + transaccion.montotransaccion
    conn.execute(cuentas.update().values(saldocuenta=nuevo_saldo).where(cuentas.c.cuentaid == transaccion.cuentaid))
    conn.commit()

    return {"message": "Depósito realizado con éxito."}

@transaccionRoute.post("/retiro", tags=["transacciones"], status_code=status.HTTP_200_OK)
def hacer_retiro(transaccion: Transaccion):
    # Verificar si la cuenta existe y pertenece al banco
    cuenta = conn.execute(select(cuentas).where(cuentas.c.cuentaid == transaccion.cuentaid)).first()
    if not cuenta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cuenta not found")

    # Verificar si la cuenta está a nombre de la persona que hace la transacción
    if cuenta.personaid != transaccion.personaid:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No estás autorizado para realizar esta transacción")

    # Verificar si la fecha de la transacción es posterior a la fecha de creación de la cuenta
    if transaccion.fechatransaccion < cuenta.fechacreacion:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La fecha de la transacción debe ser posterior a la fecha de creación de la cuenta.")

    # Obtener el banco para capturar los montos por banco
    banco = conn.execute(select(bancos).where(bancos.c.bancoid == cuenta.bancoid)).first()

    # Verificar si el monto del retiro mínimo es válido
    if transaccion.montotransaccion < banco.montomintransaccion:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"El monto del retiro debe ser mayor o igual a: {banco.montomintransaccion}")

    # Verificar si el monto del retiro máximo es válido
    if transaccion.montotransaccion > banco.montomaxtransaccion:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"El monto del retiro debe ser menor o igual a: {banco.montomaxtransaccion}")

    # Verificar si hay saldo suficiente en la cuenta
    if cuenta.saldocuenta < transaccion.montotransaccion:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No hay saldo suficiente en la cuenta. Lo sentimos")

    # Validar que el saldo restante en la cuenta no sea inferior a $100.000
    saldo_minimo = 100000
    saldo_restante = cuenta.saldocuenta - transaccion.montotransaccion

    # Obtener la fecha actual
    fecha_actual = datetime.now()

    # Convertir la fecha de creación de la cuenta a datetime
    fecha_creacion_datetime = datetime.combine(cuenta.fechacreacion, datetime.min.time())

    tiempo_transcurrido = (fecha_actual - fecha_creacion_datetime).days // 365

    saldo_minimo += banco.interesporanio * tiempo_transcurrido
    saldo_minimo += banco.cobroportransaccion
    if saldo_restante < saldo_minimo:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El saldo restante en la cuenta no puede ser inferior a $100.000")

    # Realizar el retiro
    nuevo_saldo = cuenta.saldocuenta - transaccion.montotransaccion
    conn.execute(cuentas.update().values(saldocuenta=nuevo_saldo).where(cuentas.c.cuentaid == transaccion.cuentaid))
    conn.commit()

    # Guardar la transacción en la tabla transacciones
    nueva_transaccion = {
        "montotransaccion": transaccion.montotransaccion,
        "cuentaid": transaccion.cuentaid,
        "fechatransaccion": transaccion.fechatransaccion,
        "personaid": transaccion.personaid,
        "tipotransaccionid": 1
    }
    conn.execute(insert(transacciones).values(nueva_transaccion))
    conn.commit()

    return {"message": "Retiro realizado con éxito."}