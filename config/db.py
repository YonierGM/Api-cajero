from sqlalchemy import create_engine, MetaData

engine = create_engine('postgresql://postgres:0000@localhost:5432/cajero')
meta = MetaData()
conn = engine.connect()
