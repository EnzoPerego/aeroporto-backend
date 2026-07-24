import logging

import requests

from src.config.config import config
from src.entities.voo import Voo
from src.repositories.reserva_repository import ReservaRepository

logger = logging.getLogger(__name__)

STATUS_SEM_NOTIFICACAO = ("perdeu_voo", "realocado")


def notify_status_change(reserva_repo: ReservaRepository, voo: Voo, status_anterior: str) -> None:
    """Dispara um webhook (n8n) com os passageiros do voo quando o status muda.

    Falhas de rede aqui nao devem quebrar a atualizacao do voo em si.
    """
    if not config.N8N_WEBHOOK_URL or voo.status == status_anterior:
        return

    reservas = reserva_repo.list_by_voo(voo.id)
    passageiros = [
        {"nome": r.passageiro.nome, "email": r.passageiro.email}
        for r in reservas
        if r.passageiro.email and r.status not in STATUS_SEM_NOTIFICACAO
    ]
    if not passageiros:
        return

    payload = {
        "numero_voo": voo.numero_voo,
        "origem": voo.origem,
        "destino": voo.destino,
        "status_anterior": status_anterior,
        "status_novo": voo.status,
        "passageiros": passageiros,
    }

    try:
        requests.post(config.N8N_WEBHOOK_URL, json=payload, timeout=5)
    except requests.RequestException:
        logger.warning("Falha ao notificar mudanca de status do voo %s", voo.numero_voo, exc_info=True)
