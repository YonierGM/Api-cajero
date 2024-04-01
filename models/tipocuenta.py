from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String

from config.db import meta, engine

tipocuentas = Table(

    "tipocuentas",
    meta,

    Column("tipocuentaid", Integer, primary_key=True),
    Column("descripcion", String(255))
)
meta.create_all(engine)