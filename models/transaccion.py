from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, Date

from config.db import meta, engine

from .persona import personas
from .cuenta import cuentas
from .tipotransaccion import tipotransacciones

transacciones = Table(

    "transacciones",
    meta,

    Column("transaccionid", Integer, primary_key=True),

    Column("montotransaccion", Integer),
    Column("cuentaid", Integer, ForeignKey(cuentas.c.cuentaid)),
    Column("fechatransaccion", Date),
    Column("personaid", Integer, ForeignKey(personas.c.personaid)),
    Column("tipotransaccionid", Integer, ForeignKey(tipotransacciones.c.tipotransaccionid)),
)
meta.create_all(engine)