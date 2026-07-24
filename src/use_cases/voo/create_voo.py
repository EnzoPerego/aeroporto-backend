from src.entities.voo import Voo
from src.models.voo_model import VooCreate
from src.repositories.voo_repository import VooRepository


def create_voo(repo: VooRepository, dados: VooCreate) -> Voo:
    return repo.create(**dados.model_dump())
