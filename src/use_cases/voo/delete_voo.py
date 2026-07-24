from src.repositories.voo_repository import VooRepository
from src.use_cases.voo.get_voo import get_voo


def delete_voo(repo: VooRepository, voo_id: int) -> None:
    voo = get_voo(repo, voo_id)
    repo.delete(voo)
