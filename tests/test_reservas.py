def criar_passageiro(client, documento, nome="Fulano"):
    resp = client.post("/passageiros/", json={"nome": nome, "documento": documento})
    assert resp.status_code == 201
    return resp.json()


def test_cria_reserva(client, voo, passageiro):
    resp = client.post("/reservas/", json={"passageiro_id": passageiro["id"], "voo_id": voo["id"]})
    assert resp.status_code == 201
    body = resp.json()
    assert body["status"] == "confirmado"
    assert body["realocado_de_reserva_id"] is None


def test_404_voo_inexistente_ao_criar_reserva(client, passageiro):
    resp = client.post("/reservas/", json={"passageiro_id": passageiro["id"], "voo_id": 999})
    assert resp.status_code == 404


def test_404_passageiro_inexistente_ao_criar_reserva(client, voo):
    resp = client.post("/reservas/", json={"passageiro_id": 999, "voo_id": voo["id"]})
    assert resp.status_code == 404


def test_reserva_duplicada_no_mesmo_voo_retorna_409(client, voo, passageiro):
    client.post("/reservas/", json={"passageiro_id": passageiro["id"], "voo_id": voo["id"]})
    resp = client.post("/reservas/", json={"passageiro_id": passageiro["id"], "voo_id": voo["id"]})
    assert resp.status_code == 409


def test_voo_lotado_retorna_400(client, voo, passageiro):
    # a aeronave da fixture tem capacidade_maxima=2
    p2 = criar_passageiro(client, "22222222222", "Segundo")
    p3 = criar_passageiro(client, "33333333333", "Terceiro")
    client.post("/reservas/", json={"passageiro_id": passageiro["id"], "voo_id": voo["id"]})
    client.post("/reservas/", json={"passageiro_id": p2["id"], "voo_id": voo["id"]})

    resp = client.post("/reservas/", json={"passageiro_id": p3["id"], "voo_id": voo["id"]})
    assert resp.status_code == 400


def test_atualiza_status_reserva(client, voo, passageiro):
    reserva = client.post(
        "/reservas/", json={"passageiro_id": passageiro["id"], "voo_id": voo["id"]}
    ).json()
    resp = client.patch(f"/reservas/{reserva['id']}", json={"status": "checkin_feito"})
    assert resp.status_code == 200
    assert resp.json()["status"] == "checkin_feito"


def test_remove_reserva_remove_mala_em_cascata(client, voo, passageiro):
    reserva = client.post(
        "/reservas/", json={"passageiro_id": passageiro["id"], "voo_id": voo["id"]}
    ).json()
    mala = client.post(
        "/malas/", json={"codigo_identificacao": "BAG-777", "reserva_id": reserva["id"]}
    ).json()

    resp = client.delete(f"/reservas/{reserva['id']}")
    assert resp.status_code == 204
    assert client.get(f"/malas/{mala['id']}").status_code == 404


def test_realocar_reserva_cria_nova_e_preserva_historico(client, terminal, gate, aeronave, passageiro):
    voo1 = client.post(
        "/voos/",
        json={
            "numero_voo": "CT101",
            "origem": "Cape Town",
            "destino": "Johannesburg",
            "aeronave_id": aeronave["id"],
            "terminal_id": terminal["id"],
        },
    ).json()
    voo2 = client.post(
        "/voos/",
        json={
            "numero_voo": "CT202",
            "origem": "Cape Town",
            "destino": "London",
            "aeronave_id": aeronave["id"],
            "terminal_id": terminal["id"],
        },
    ).json()
    reserva_original = client.post(
        "/reservas/", json={"passageiro_id": passageiro["id"], "voo_id": voo1["id"]}
    ).json()

    resp = client.post(f"/reservas/{reserva_original['id']}/realocar", json={"novo_voo_id": voo2["id"]})
    assert resp.status_code == 201
    nova_reserva = resp.json()
    assert nova_reserva["voo_id"] == voo2["id"]
    assert nova_reserva["status"] == "confirmado"
    assert nova_reserva["realocado_de_reserva_id"] == reserva_original["id"]

    original_atualizada = client.get(f"/reservas/{reserva_original['id']}").json()
    assert original_atualizada["status"] == "realocado"


def test_realocar_para_voo_inexistente_404(client, voo, passageiro):
    reserva = client.post(
        "/reservas/", json={"passageiro_id": passageiro["id"], "voo_id": voo["id"]}
    ).json()
    resp = client.post(f"/reservas/{reserva['id']}/realocar", json={"novo_voo_id": 999})
    assert resp.status_code == 404


def test_lista_e_404_reserva(client, voo, passageiro):
    assert client.get("/reservas/").json() == []
    assert client.get("/reservas/999").status_code == 404
