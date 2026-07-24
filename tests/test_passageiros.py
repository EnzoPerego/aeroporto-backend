def test_cria_passageiro(client):
    resp = client.post(
        "/passageiros/", json={"nome": "Bruno Costa", "documento": "22222222222", "email": None}
    )
    assert resp.status_code == 201
    assert resp.json()["email"] is None


def test_lista_passageiros(client, passageiro):
    resp = client.get("/passageiros/")
    assert resp.status_code == 200
    assert len(resp.json()) == 1


def test_404_passageiro_inexistente(client):
    assert client.get("/passageiros/999").status_code == 404


def test_atualiza_passageiro(client, passageiro):
    resp = client.put(
        f"/passageiros/{passageiro['id']}",
        json={"nome": "Ana Silva Souza", "documento": passageiro["documento"], "email": "nova@example.com"},
    )
    assert resp.status_code == 200
    assert resp.json()["nome"] == "Ana Silva Souza"


def test_remove_passageiro_sem_reservas(client, passageiro):
    resp = client.delete(f"/passageiros/{passageiro['id']}")
    assert resp.status_code == 204


def test_remove_passageiro_com_reserva_e_mala_cascade(client, passageiro, voo):
    reserva = client.post(
        "/reservas/", json={"passageiro_id": passageiro["id"], "voo_id": voo["id"]}
    ).json()
    mala = client.post(
        "/malas/", json={"codigo_identificacao": "BAG-999", "reserva_id": reserva["id"]}
    ).json()

    resp = client.delete(f"/passageiros/{passageiro['id']}")
    assert resp.status_code == 204

    # reserva e mala devem ter sido removidas em cascata, nao deixando registros orfaos
    assert client.get(f"/reservas/{reserva['id']}").status_code == 404
    assert client.get(f"/malas/{mala['id']}").status_code == 404
