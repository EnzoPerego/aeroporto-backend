from src.entities.voo import Voo
from src.models.voo_model import VooUpdate
from src.repositories.voo_repository import VooRepository
from src.use_cases.voo.get_voo import get_voo


def update_voo(repo: VooRepository, voo_id: int, dados: VooUpdate) -> Voo:
    voo = get_voo(repo, voo_id)
    return repo.update(voo, **dados.model_dump(exclude_unset=True))
