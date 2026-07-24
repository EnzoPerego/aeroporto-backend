from src.entities.voo import Voo
from src.repositories.voo_repository import VooRepository


def list_voos(repo: VooRepository) -> list[Voo]:
    return repo.list_all()
