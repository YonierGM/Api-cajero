from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String, Date

from config.db import meta, engine

from .banco import bancos
from .persona import personas
from .tipocuenta import tipocuentas

cuentas = Table(

    "cuentas",
    meta,

    Column("cuentaid", Integer, primary_key=True),

    Column("bancoid", Integer, ForeignKey(bancos.c.bancoid)),
    Column("personaid", Integer, ForeignKey(personas.c.personaid)),
    Column("tipocuentaid", Integer, ForeignKey(tipocuentas.c.tipocuentaid)),

    Column("numerocuenta", Integer),
    Column("saldocuenta", Integer),
    Column("fechacreacion", Date),
)
meta.create_all(engine)