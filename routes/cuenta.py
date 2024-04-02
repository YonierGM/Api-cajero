from fastapi import APIRouter, HTTPException, status, Response
from typing import List
from sqlalchemy import insert, select, update, delete
from datetime import datetime

from config.db import conn
from schemas.cuenta import Cuenta

#importo bancos para verificar si existe uno al momento de crear cuenta
from models.banco import bancos

from models.cuenta import cuentas


cuentasRoute = APIRouter()
def calcular_tiempo_transcurrido(fecha_creacion):
    fecha_actual = datetime.now()

    # Convertir fecha_creacion a datetime
    fecha_creacion_datetime = datetime.combine(fecha_creacion, datetime.min.time())

    # Calcular diferencia entre las fechas
    diferencia = fecha_actual - fecha_creacion_datetime

    # Calcular días completos, semanas completas y meses completos
    anios_completos = diferencia.days // 365
    meses_completos = diferencia.days // 30
    semanas_completas = diferencia.days // 7
    dias_completos = diferencia.days

    # Generar mensaje basado en el tiempo transcurrido
    if anios_completos >= 1:
        if anios_completos == 1:
            return "1 año"
        else:
            return f"{anios_completos} años"
    elif meses_completos >= 1:
        if meses_completos == 1:
            return "1 mes"
        else:
            return f"{meses_completos} meses"
    elif semanas_completas >= 1:
        if semanas_completas == 1:
            return "1 semana"
        else:
            return f"{semanas_completas} semanas"

    else:
        if dias_completos < 1:
            return "menos de 1 día"
        else:
            return f"{dias_completos} días"

@cuentasRoute.get('/cuentas', tags=['cuentas'], response_model=List[Cuenta])
def get_cuentas():
    return conn.execute(select(cuentas)).fetchall()

@cuentasRoute.get("/cuentas/{id}", tags=["cuentas"], response_model=Cuenta)
def get_cuenta(id: int):
    existing_cuenta = conn.execute(select(cuentas).where(cuentas.c.cuentaid == id)).first()
    if existing_cuenta:
        return existing_cuenta
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cuenta not found")

@cuentasRoute.post("/cuentas", tags=["cuentas"], response_model=Cuenta)
def create_cuenta(cuenta: Cuenta):
    existing_banco = conn.execute(select(bancos).where(bancos.c.bancoid == cuenta.bancoid)).first()
    if existing_banco:
        if cuenta.tipocuentaid == 1:
            existing_cuenta_ahorros = conn.execute(
                select(cuentas).where(cuentas.c.tipocuentaid == 1 and cuentas.c.personaid == cuenta.personaid)).first()
            if existing_cuenta_ahorros:
                tiempo_transcurrido = calcular_tiempo_transcurrido(existing_cuenta_ahorros.fechacreacion)
                raise HTTPException(status_code=400, detail="Ya tiene una cuenta de ahorros creada anteriormente con un saldo de: " + str(existing_cuenta_ahorros.saldocuenta) + " creada hace: " + str(tiempo_transcurrido)+" fecha crea: "+str(cuenta.fechacreacion))

        # Verificar si la cuenta es de tipo corriente
        if cuenta.tipocuentaid == 2:

            # Verificar si el número total de cuentas corrientes en diferentes bancos excede 6
            cuentas_totales_corriente = conn.execute(
                select(cuentas)
                .where(cuentas.c.tipocuentaid == 2 and cuentas.c.personaid == cuenta.personaid)
            ).fetchall()
            if len(cuentas_totales_corriente) >= 6:
                raise HTTPException(
                    status_code=400,
                    detail="Ya tiene el máximo de cuentas corrientes en diferentes bancos: " + str(
                        len(cuentas_totales_corriente))
                )

            # Verificar si el número de cuentas corrientes en el mismo banco excede 3
            cuentas_corriente_por_banco = conn.execute(
                select(cuentas)
                .where((cuentas.c.tipocuentaid == 2) & (cuentas.c.bancoid == cuenta.bancoid))
            ).fetchall()
            if len(cuentas_corriente_por_banco) >= 3:
                print(cuenta.bancoid)
                raise HTTPException(
                    status_code=400,
                    detail="Ya tiene el máximo de cuentas corrientes en este banco: " + str(
                        len(cuentas_corriente_por_banco))
                )
        try:

            new_cuenta = {
                "bancoid": cuenta.bancoid,
                "personaid": cuenta.personaid,
                "tipocuentaid": cuenta.tipocuentaid,
                "numerocuenta": cuenta.numerocuenta,
                "saldocuenta": cuenta.saldocuenta,
                "fechacreacion": cuenta.fechacreacion,
            }
            result = conn.execute(insert(cuentas).values(new_cuenta))
            new_cuenta_id = result.inserted_primary_key[0]

            # Actualizar el campo cantcuentas en la tabla bancos
            conn.execute(
                update(bancos)
                .values(cantcuentas=existing_banco.cantcuentas + 1)
                .where(bancos.c.bancoid == cuenta.bancoid)
            )

            conn.commit()
            # Obtener la cuenta recién creada
            new_cuenta = conn.execute(select(cuentas).where(cuentas.c.cuentaid == new_cuenta_id)).fetchone()

            return new_cuenta
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    else:
        raise HTTPException(status_code=404, detail="El banco especificado no existe.")

@cuentasRoute.put("/cuentas/{id}", tags=["cuentas"], response_model=Cuenta)
def update_cuenta(id: int, cuenta: Cuenta):
    existing_cuenta = conn.execute(select(cuentas).where(cuentas.c.cuentaid == id)).fetchone()
    if existing_cuenta:
        conn.execute(
            update(cuentas)
            .values(
                bancoid=cuenta.bancoid,
                personaid=cuenta.personaid,
                tipocuentaid=cuenta.tipocuentaid,
                numerocuenta=cuenta.numerocuenta,
                saldocuenta=cuenta.saldocuenta,
                fechacreacion=cuenta.fechacreacion,
            )
            .where(cuentas.c.cuentaid == id)
        )
        conn.commit()
        cuenta_updated = conn.execute(select(cuentas).where(cuentas.c.cuentaid == id)).fetchone()
        return cuenta_updated
    else:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cuenta not found")

@cuentasRoute.delete("/cuentas/{id}", tags=["cuentas"])
def delete_cuenta(id: int):

    existing_cuenta = conn.execute(select(cuentas).where(cuentas.c.cuentaid == id)).fetchone()
    if existing_cuenta:
        existing_banco = conn.execute(select(bancos).where(bancos.c.bancoid == existing_cuenta.bancoid)).fetchone()
        if existing_banco:
            mensaje = ""
            if existing_cuenta.saldocuenta < 0:
                return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cuenta con saldo negativo, no se puede eliminar")

            elif existing_cuenta.saldocuenta != 0:
                return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                     detail="La cuenta aún tiene saldo, no se puede eliminar")

            # Obtener el ID del banco asociado a la cuenta
            bancoid = existing_cuenta.bancoid

            # Eliminar la cuenta
            conn.execute(delete(cuentas).where(cuentas.c.cuentaid == id))

            # Actualizar el campo cantcuentas en la tabla bancos
            conn.execute(
                update(bancos)
                .values(cantcuentas=bancos.c.cantcuentas - 1)  # Restar 1 al campo cantcuentas
                .where(bancos.c.bancoid == bancoid)
            )

            if existing_cuenta.tipocuentaid == 2:
                cuentas_corrientes = conn.execute(
                    select(cuentas)
                    .where(cuentas.c.tipocuentaid == 2 and
                           cuentas.c.personaid == existing_cuenta.personaid and
                           cuentas.c.cuentaid != existing_cuenta.cuentaid)).fetchall()

                # Itera sobre los resultados y muestra la información
                for cuenta in cuentas_corrientes:
                    numerocuenta = cuenta.numerocuenta
                    saldocuenta = cuenta.saldocuenta
                    fechacreacion = cuenta.fechacreacion

                    tiempo_transcurrido = calcular_tiempo_transcurrido(fechacreacion)
                    mensaje += f"Número de cuenta: {numerocuenta}, Saldo: {saldocuenta}, Creada hace: {tiempo_transcurrido}\n"


            conn.commit()
            if cuentas_corrientes:
                return Response(status_code=status.HTTP_200_OK, content=mensaje)

            else:
                return status.HTTP_200_OK

        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Banco not found")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cuenta not found")
