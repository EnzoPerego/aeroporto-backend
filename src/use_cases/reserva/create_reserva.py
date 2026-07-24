from fastapi import HTTPException

from src.entities.reserva import Reserva
from src.models.reserva_model import ReservaCreate
from src.repositories.passageiro_repository import PassageiroRepository
from src.repositories.reserva_repository import ReservaRepository
from src.repositories.voo_repository import VooRepository


def create_reserva(
    reserva_repo: ReservaRepository,
    voo_repo: VooRepository,
    passageiro_repo: PassageiroRepository,
    dados: ReservaCreate,
) -> Reserva:
    voo = voo_repo.get(dados.voo_id)
    if not voo:
        raise HTTPException(status_code=404, detail="Voo não encontrado")
    if not passageiro_repo.get(dados.passageiro_id):
        raise HTTPException(status_code=404, detail="Passageiro não encontrado")

    if reserva_repo.find_by_passageiro_e_voo(dados.passageiro_id, dados.voo_id):
        raise HTTPException(status_code=409, detail="Passageiro já possui reserva neste voo")

    ocupados = reserva_repo.contar_assentos_ocupados(voo.id)
    if ocupados >= voo.aeronave.capacidade_maxima:
        raise HTTPException(status_code=400, detail="Voo sem assentos disponíveis")

    return reserva_repo.create(**dados.model_dump())
