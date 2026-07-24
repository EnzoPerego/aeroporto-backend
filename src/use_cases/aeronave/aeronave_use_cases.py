from fastapi import HTTPException

from src.entities.aeronave import Aeronave
from src.models.aeronave_model import AeronaveCreate, AeronaveOcupacao
from src.repositories.aeronave_repository import AeronaveRepository
from src.repositories.reserva_repository import ReservaRepository
from src.repositories.voo_repository import VooRepository


def list_aeronaves(repo: AeronaveRepository) -> list[Aeronave]:
    return repo.list_all()


def get_aeronave(repo: AeronaveRepository, aeronave_id: int) -> Aeronave:
    aeronave = repo.get(aeronave_id)
    if not aeronave:
        raise HTTPException(status_code=404, detail="Aeronave não encontrada")
    return aeronave


def create_aeronave(repo: AeronaveRepository, dados: AeronaveCreate) -> Aeronave:
    return repo.create(**dados.model_dump())


def update_aeronave(repo: AeronaveRepository, aeronave_id: int, dados: AeronaveCreate) -> Aeronave:
    aeronave = get_aeronave(repo, aeronave_id)
    return repo.update(aeronave, **dados.model_dump())


def delete_aeronave(repo: AeronaveRepository, aeronave_id: int) -> None:
    aeronave = get_aeronave(repo, aeronave_id)
    repo.delete(aeronave)


def get_ocupacao_aeronave(
    aeronave_repo: AeronaveRepository,
    voo_repo: VooRepository,
    reserva_repo: ReservaRepository,
    aeronave_id: int,
) -> AeronaveOcupacao:
    aeronave = get_aeronave(aeronave_repo, aeronave_id)
    voo_ativo = voo_repo.find_ativo_por_aeronave(aeronave_id)
    ocupados = reserva_repo.contar_assentos_ocupados(voo_ativo.id) if voo_ativo else 0

    return AeronaveOcupacao(
        aeronave_id=aeronave.id,
        capacidade_maxima=aeronave.capacidade_maxima,
        assentos_ocupados=ocupados,
        assentos_disponiveis=aeronave.capacidade_maxima - ocupados,
    )
