from src.models.aeronave_model import AeronaveOcupacao
from src.repositories.reserva_repository import ReservaRepository
from src.repositories.voo_repository import VooRepository
from src.use_cases.voo.get_voo import get_voo


def get_ocupacao_voo(
    voo_repo: VooRepository, reserva_repo: ReservaRepository, voo_id: int
) -> AeronaveOcupacao:
    voo = get_voo(voo_repo, voo_id)
    ocupados = reserva_repo.contar_assentos_ocupados(voo_id)
    capacidade = voo.aeronave.capacidade_maxima

    return AeronaveOcupacao(
        aeronave_id=voo.aeronave_id,
        capacidade_maxima=capacidade,
        assentos_ocupados=ocupados,
        assentos_disponiveis=capacidade - ocupados,
    )
