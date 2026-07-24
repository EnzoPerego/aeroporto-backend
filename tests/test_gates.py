def test_cria_gate(client, terminal):
    resp = client.post("/gates/", json={"codigo": "B2", "terminal_id": terminal["id"]})
    assert resp.status_code == 201
    body = resp.json()
    assert body["codigo"] == "B2"
    assert body["status"] == "livre"


def test_lista_gates(client, gate):
    resp = client.get("/gates/")
    assert resp.status_code == 200
    assert len(resp.json()) == 1


def test_404_gate_inexistente(client):
    assert client.get("/gates/999").status_code == 404


def test_atualiza_status_gate_parcial(client, gate):
    resp = client.patch(f"/gates/{gate['id']}", json={"status": "ocupado"})
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "ocupado"
    assert body["codigo"] == gate["codigo"]  # nao mudou, era um update parcial


def test_remove_gate(client, gate):
    resp = client.delete(f"/gates/{gate['id']}")
    assert resp.status_code == 204
    assert client.get(f"/gates/{gate['id']}").status_code == 404
