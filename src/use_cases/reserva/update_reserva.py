from src.entities.reserva import Reserva
from src.models.reserva_model import ReservaUpdate
from src.repositories.reserva_repository import ReservaRepository
from src.use_cases.reserva.get_reserva import get_reserva


def update_reserva(repo: ReservaRepository, reserva_id: int, dados: ReservaUpdate) -> Reserva:
    reserva = get_reserva(repo, reserva_id)
    return repo.update(reserva, **dados.model_dump(exclude_unset=True))
