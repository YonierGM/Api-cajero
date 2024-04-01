from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String

from config.db import meta, engine

bancos = Table(

    "bancos",
    meta,

    Column("bancoid", Integer, primary_key=True),
    Column("numerobanco", Integer),
    Column("nombre", String(255)),
    Column("cantcuentas", Integer),
    Column("montomaxtransaccion", Integer),
    Column("montomintransaccion", Integer),
    Column("cobroportransaccion", Integer),
    Column("interesporanio", Integer),
)
meta.create_all(engine)