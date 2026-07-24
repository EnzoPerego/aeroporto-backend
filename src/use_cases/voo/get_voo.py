from fastapi import HTTPException

from src.entities.voo import Voo
from src.repositories.voo_repository import VooRepository


def get_voo(repo: VooRepository, voo_id: int) -> Voo:
    voo = repo.get(voo_id)
    if not voo:
        raise HTTPException(status_code=404, detail="Voo não encontrado")
    return voo
