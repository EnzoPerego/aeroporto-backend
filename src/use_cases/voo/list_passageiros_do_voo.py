from src.entities.reserva import Reserva
from src.repositories.reserva_repository import ReservaRepository
from src.repositories.voo_repository import VooRepository
from src.use_cases.voo.get_voo import get_voo


def list_passageiros_do_voo(
    voo_repo: VooRepository, reserva_repo: ReservaRepository, voo_id: int
) -> list[Reserva]:
    get_voo(voo_repo, voo_id)
    return reserva_repo.list_by_voo(voo_id)
