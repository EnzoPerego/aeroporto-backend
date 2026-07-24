import os
import tempfile

# Precisa ser definido ANTES de qualquer import de src.*, pois src/config/config.py
# le a variavel de ambiente no momento da importacao do modulo.
os.environ["DATABASE_URL"] = f"sqlite:///{tempfile.mktemp(suffix='.db')}"
os.environ.setdefault("N8N_WEBHOOK_URL", "")

import pytest
from fastapi.testclient import TestClient

from src import entities  # noqa: F401  garante que todas as entities sejam registradas
from src.app import app
from src.database.database import Base, engine


@pytest.fixture(autouse=True)
def banco_limpo():
    """Recria o schema do zero antes de cada teste, garantindo isolamento total."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture
def terminal(client):
    resp = client.post("/terminais/", json={"nome": "Terminal 1", "tipo": "nacional"})
    assert resp.status_code == 201
    return resp.json()


@pytest.fixture
def gate(client, terminal):
    resp = client.post("/gates/", json={"codigo": "A1", "terminal_id": terminal["id"]})
    assert resp.status_code == 201
    return resp.json()


@pytest.fixture
def aeronave(client):
    resp = client.post(
        "/aeronaves/",
        json={"modelo": "Airbus A320", "matricula": "PR-ABC", "capacidade_maxima": 2},
    )
    assert resp.status_code == 201
    return resp.json()


@pytest.fixture
def voo(client, terminal, gate, aeronave):
    resp = client.post(
        "/voos/",
        json={
            "numero_voo": "CT101",
            "origem": "Cape Town",
            "destino": "Johannesburg",
            "aeronave_id": aeronave["id"],
            "terminal_id": terminal["id"],
            "gate_id": gate["id"],
        },
    )
    assert resp.status_code == 201
    return resp.json()


@pytest.fixture
def passageiro(client):
    resp = client.post(
        "/passageiros/", json={"nome": "Ana Silva", "documento": "11111111111", "email": "ana@example.com"}
    )
    assert resp.status_code == 201
    return resp.json()
