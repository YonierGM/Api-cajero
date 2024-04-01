from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from routes.persona import personasRoute
from routes.banco import bancosRoute
from routes.cuenta import cuentasRoute
from routes.tipocuenta import tipocuentasRoute

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

app.include_router(personasRoute),
app.include_router(bancosRoute),
app.include_router(cuentasRoute),
app.include_router(tipocuentasRoute)