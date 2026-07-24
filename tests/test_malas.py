import pytest


@pytest.fixture
def reserva(client, voo, passageiro):
    resp = client.post("/reservas/", json={"passageiro_id": passageiro["id"], "voo_id": voo["id"]})
    assert resp.status_code == 201
    return resp.json()


def test_cria_mala(client, reserva):
    resp = client.post(
        "/malas/", json={"codigo_identificacao": "BAG-0001", "reserva_id": reserva["id"]}
    )
    assert resp.status_code == 201
    assert resp.json()["status"] == "despachada"


def test_404_reserva_inexistente_ao_criar_mala(client):
    resp = client.post("/malas/", json={"codigo_identificacao": "BAG-0002", "reserva_id": 999})
    assert resp.status_code == 404


def test_lista_malas(client, reserva):
    client.post("/malas/", json={"codigo_identificacao": "BAG-0003", "reserva_id": reserva["id"]})
    resp = client.get("/malas/")
    assert resp.status_code == 200
    assert len(resp.json()) == 1


def test_404_mala_inexistente(client):
    assert client.get("/malas/999").status_code == 404


def test_atualiza_status_mala(client, reserva):
    mala = client.post(
        "/malas/", json={"codigo_identificacao": "BAG-0004", "reserva_id": reserva["id"]}
    ).json()
    resp = client.patch(f"/malas/{mala['id']}", json={"status": "extraviada"})
    assert resp.status_code == 200
    assert resp.json()["status"] == "extraviada"


def test_remove_mala(client, reserva):
    mala = client.post(
        "/malas/", json={"codigo_identificacao": "BAG-0005", "reserva_id": reserva["id"]}
    ).json()
    resp = client.delete(f"/malas/{mala['id']}")
    assert resp.status_code == 204
    assert client.get(f"/malas/{mala['id']}").status_code == 404
