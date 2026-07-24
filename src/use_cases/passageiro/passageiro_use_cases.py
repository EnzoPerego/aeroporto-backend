from fastapi import HTTPException

from src.entities.passageiro import Passageiro
from src.models.passageiro_model import PassageiroCreate
from src.repositories.passageiro_repository import PassageiroRepository


def list_passageiros(repo: PassageiroRepository) -> list[Passageiro]:
    return repo.list_all()


def get_passageiro(repo: PassageiroRepository, passageiro_id: int) -> Passageiro:
    passageiro = repo.get(passageiro_id)
    if not passageiro:
        raise HTTPException(status_code=404, detail="Passageiro não encontrado")
    return passageiro


def create_passageiro(repo: PassageiroRepository, dados: PassageiroCreate) -> Passageiro:
    return repo.create(**dados.model_dump())


def update_passageiro(
    repo: PassageiroRepository, passageiro_id: int, dados: PassageiroCreate
) -> Passageiro:
    passageiro = get_passageiro(repo, passageiro_id)
    return repo.update(passageiro, **dados.model_dump())


def delete_passageiro(repo: PassageiroRepository, passageiro_id: int) -> None:
    passageiro = get_passageiro(repo, passageiro_id)
    repo.delete(passageiro)
