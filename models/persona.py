from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String

from config.db import meta, engine

personas = Table(

    "personas",
    meta,

    Column("personaid", Integer, primary_key=True, autoincrement=True),
    Column("nombre", String(255)),
    Column("apellido", String(255)),
    Column("cedula", Integer),
    Column("profesion", String(255))
)

meta.create_all(engine)