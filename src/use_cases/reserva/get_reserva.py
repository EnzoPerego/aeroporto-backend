from fastapi import HTTPException

from src.entities.reserva import Reserva
from src.repositories.reserva_repository import ReservaRepository


def get_reserva(repo: ReservaRepository, reserva_id: int) -> Reserva:
    reserva = repo.get(reserva_id)
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva não encontrada")
    return reserva
