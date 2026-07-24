def test_lista_vazia_inicialmente(client):
    resp = client.get("/terminais/")
    assert resp.status_code == 200
    assert resp.json() == []


def test_cria_terminal(client):
    resp = client.post("/terminais/", json={"nome": "Terminal 2", "tipo": "internacional"})
    assert resp.status_code == 201
    body = resp.json()
    assert body["nome"] == "Terminal 2"
    assert body["tipo"] == "internacional"
    assert "id" in body


def test_obtem_terminal_por_id(client, terminal):
    resp = client.get(f"/terminais/{terminal['id']}")
    assert resp.status_code == 200
    assert resp.json()["nome"] == terminal["nome"]


def test_404_terminal_inexistente(client):
    resp = client.get("/terminais/999")
    assert resp.status_code == 404


def test_atualiza_terminal(client, terminal):
    resp = client.put(
        f"/terminais/{terminal['id']}", json={"nome": "Terminal 1 Renovado", "tipo": "nacional"}
    )
    assert resp.status_code == 200
    assert resp.json()["nome"] == "Terminal 1 Renovado"


def test_remove_terminal(client, terminal):
    resp = client.delete(f"/terminais/{terminal['id']}")
    assert resp.status_code == 204
    assert client.get(f"/terminais/{terminal['id']}").status_code == 404
