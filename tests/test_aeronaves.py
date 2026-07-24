def test_cria_aeronave(client):
    resp = client.post(
        "/aeronaves/",
        json={"modelo": "Boeing 787", "matricula": "PR-XYZ", "capacidade_maxima": 250},
    )
    assert resp.status_code == 201
    body = resp.json()
    assert body["capacidade_maxima"] == 250


def test_lista_aeronaves(client, aeronave):
    resp = client.get("/aeronaves/")
    assert resp.status_code == 200
    assert len(resp.json()) == 1


def test_404_aeronave_inexistente(client):
    assert client.get("/aeronaves/999").status_code == 404


def test_atualiza_aeronave(client, aeronave):
    resp = client.put(
        f"/aeronaves/{aeronave['id']}",
        json={"modelo": "Airbus A321", "matricula": aeronave["matricula"], "capacidade_maxima": 220},
    )
    assert resp.status_code == 200
    assert resp.json()["capacidade_maxima"] == 220


def test_remove_aeronave(client, aeronave):
    resp = client.delete(f"/aeronaves/{aeronave['id']}")
    assert resp.status_code == 204
    assert client.get(f"/aeronaves/{aeronave['id']}").status_code == 404


def test_ocupacao_sem_voo_ativo(client, aeronave):
    resp = client.get(f"/aeronaves/{aeronave['id']}/ocupacao")
    assert resp.status_code == 200
    body = resp.json()
    assert body["assentos_ocupados"] == 0
    assert body["assentos_disponiveis"] == aeronave["capacidade_maxima"]


def test_ocupacao_com_reservas(client, voo, passageiro, aeronave):
    client.post("/reservas/", json={"passageiro_id": passageiro["id"], "voo_id": voo["id"]})
    resp = client.get(f"/aeronaves/{aeronave['id']}/ocupacao")
    assert resp.status_code == 200
    body = resp.json()
    assert body["assentos_ocupados"] == 1
    assert body["assentos_disponiveis"] == aeronave["capacidade_maxima"] - 1
