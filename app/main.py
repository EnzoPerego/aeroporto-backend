from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import models  # noqa: F401  (garante que os models sejam registrados no Base)
from app.database import Base, engine
from app.routers import aeronaves, gates, malas, passageiros, reservas, terminais, voos

app = FastAPI(title="Plataforma de Gestão Operacional de Aeroporto")


@app.on_event("startup")
def criar_tabelas():
    Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(terminais.router)
app.include_router(gates.router)
app.include_router(aeronaves.router)
app.include_router(voos.router)
app.include_router(passageiros.router)
app.include_router(reservas.router)
app.include_router(malas.router)


@app.get("/")
def root():
    return {"status": "ok"}
