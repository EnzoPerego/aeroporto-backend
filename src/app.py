from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routers import aeronaves, gates, malas, passageiros, reservas, terminais, voos

app = FastAPI(title="Plataforma de Gestão Operacional de Aeroporto")

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
