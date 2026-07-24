from src.repositories.reserva_repository import ReservaRepository
from src.use_cases.reserva.get_reserva import get_reserva


def delete_reserva(repo: ReservaRepository, reserva_id: int) -> None:
    reserva = get_reserva(repo, reserva_id)
    repo.delete(reserva)
