from fastapi import APIRouter, HTTPException, status

from typing import List
from sqlalchemy import insert

from config.db import conn

from schemas.persona import Persona
from models.persona import personas

personasRoute = APIRouter()

@personasRoute.get('/login', tags=['personas'], response_model=Persona)
def login(email: str, passw: str):
    login = conn.execute(personas.select().where((personas.c.email == email) & (personas.c.passw == passw))).first()
    print(passw)
    print(email)
    if login:
        return login
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Datos Erroneos")

@personasRoute.get('/personas', tags=['personas'], response_model=List[Persona])
def get_personas():
    return conn.execute(personas.select()).fetchall()

@personasRoute.get("/personas/{id}", tags=["personas"], response_model=Persona)
def get_persona(id: int):
    existing_persona = conn.execute(personas.select().where(personas.c.personaid == id)).first()
    if existing_persona:
        return existing_persona
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Persona not found")

@personasRoute.post("/personas", tags=["personas"], response_model=Persona)
def create_persona(persona: Persona):
    try:
        new_persona = {
            "nombre": persona.nombre,
            "apellido": persona.apellido,
            "cedula": persona.cedula,
            "profesion": persona.profesion,
            "email": persona.email,
            "passw": persona.passw
        }
        result = conn.execute(insert(personas).values(new_persona))
        new_persona["personaid"] = result.inserted_primary_key[0]
        conn.commit()
        return new_persona
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@personasRoute.put("/personas/{id}", tags=["personas"], response_model=Persona)
def update_persona(id: int, persona: Persona):
    existing_persona = conn.execute(personas.select().where(personas.c.personaid == id)).fetchone()
    if existing_persona:
        conn.execute(
            personas.update()
            .values(
                nombre=persona.nombre,
                apellido=persona.apellido,
                cedula=persona.cedula,
                profesion=persona.profesion,
                email=persona.email,
                passw=persona.passw
            )
            .where(personas.c.personaid == id)
        )
        conn.commit()
        persona_updated = conn.execute(personas.select().where(personas.c.personaid == id)).fetchone()
        return persona_updated
    else:
         return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Persona not found")

@personasRoute.delete("/personas/{id}", tags=["personas"])
def delete_personas(id: int):
    existing_personas = conn.execute(personas.select().where(personas.c.administradorid == id)).fetchone()
    if existing_personas:
        conn.execute(personas.delete().where(personas.c.administradorid == id))
        conn.commit()
        return status.HTTP_200_OK
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="persona not found")