from src.entities.reserva import Reserva
from src.repositories.reserva_repository import ReservaRepository


def list_reservas(repo: ReservaRepository) -> list[Reserva]:
    return repo.list_all()
