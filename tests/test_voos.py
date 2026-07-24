def test_cria_voo(client, terminal, gate, aeronave):
    resp = client.post(
        "/voos/",
        json={
            "numero_voo": "CT202",
            "origem": "Cape Town",
            "destino": "London",
            "aeronave_id": aeronave["id"],
            "terminal_id": terminal["id"],
            "gate_id": gate["id"],
        },
    )
    assert resp.status_code == 201
    assert resp.json()["status"] == "no_horario"


def test_voo_sem_gate_e_valido(client, terminal, aeronave):
    resp = client.post(
        "/voos/",
        json={
            "numero_voo": "CT303",
            "origem": "Cape Town",
            "destino": "Durban",
            "aeronave_id": aeronave["id"],
            "terminal_id": terminal["id"],
        },
    )
    assert resp.status_code == 201
    assert resp.json()["gate_id"] is None


def test_lista_voos(client, voo):
    resp = client.get("/voos/")
    assert resp.status_code == 200
    assert len(resp.json()) == 1


def test_404_voo_inexistente(client):
    assert client.get("/voos/999").status_code == 404


def test_atualiza_status_voo_parcial(client, voo):
    resp = client.patch(f"/voos/{voo['id']}", json={"status": "atrasado"})
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "atrasado"
    assert body["numero_voo"] == voo["numero_voo"]


def test_remove_voo(client, voo):
    resp = client.delete(f"/voos/{voo['id']}")
    assert resp.status_code == 204
    assert client.get(f"/voos/{voo['id']}").status_code == 404


def test_ocupacao_voo(client, voo, passageiro, aeronave):
    client.post("/reservas/", json={"passageiro_id": passageiro["id"], "voo_id": voo["id"]})
    resp = client.get(f"/voos/{voo['id']}/ocupacao")
    assert resp.status_code == 200
    body = resp.json()
    assert body["capacidade_maxima"] == aeronave["capacidade_maxima"]
    assert body["assentos_ocupados"] == 1


def test_passageiros_do_voo_vazio(client, voo):
    resp = client.get(f"/voos/{voo['id']}/passageiros")
    assert resp.status_code == 200
    assert resp.json() == []


def test_passageiros_do_voo_com_reserva(client, voo, passageiro):
    client.post("/reservas/", json={"passageiro_id": passageiro["id"], "voo_id": voo["id"]})
    resp = client.get(f"/voos/{voo['id']}/passageiros")
    assert resp.status_code == 200
    body = resp.json()
    assert len(body) == 1
    assert body[0]["passageiro"]["nome"] == passageiro["nome"]
