from fastapi import HTTPException

from src.entities.mala import Mala
from src.models.mala_model import MalaCreate, MalaUpdate
from src.repositories.mala_repository import MalaRepository
from src.repositories.reserva_repository import ReservaRepository


def list_malas(repo: MalaRepository) -> list[Mala]:
    return repo.list_all()


def get_mala(repo: MalaRepository, mala_id: int) -> Mala:
    mala = repo.get(mala_id)
    if not mala:
        raise HTTPException(status_code=404, detail="Mala não encontrada")
    return mala


def create_mala(repo: MalaRepository, reserva_repo: ReservaRepository, dados: MalaCreate) -> Mala:
    if not reserva_repo.get(dados.reserva_id):
        raise HTTPException(status_code=404, detail="Reserva não encontrada")
    return repo.create(**dados.model_dump())


def update_mala(repo: MalaRepository, mala_id: int, dados: MalaUpdate) -> Mala:
    mala = get_mala(repo, mala_id)
    return repo.update(mala, **dados.model_dump(exclude_unset=True))


def delete_mala(repo: MalaRepository, mala_id: int) -> None:
    mala = get_mala(repo, mala_id)
    repo.delete(mala)
