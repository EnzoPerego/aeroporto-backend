from typing import List, Optional

from src.entities.reserva import Reserva
from src.repositories.base_repository import BaseRepository

STATUS_OCUPA_ASSENTO = ("confirmado", "checkin_feito", "embarcado")


class ReservaRepository(BaseRepository[Reserva]):
    model = Reserva

    def find_by_passageiro_e_voo(self, passageiro_id: int, voo_id: int) -> Optional[Reserva]:
        return (
            self.db.query(Reserva)
            .filter(Reserva.passageiro_id == passageiro_id, Reserva.voo_id == voo_id)
            .first()
        )

    def list_by_voo(self, voo_id: int) -> List[Reserva]:
        return self.db.query(Reserva).filter(Reserva.voo_id == voo_id).all()

    def contar_assentos_ocupados(self, voo_id: int) -> int:
        return (
            self.db.query(Reserva)
            .filter(Reserva.voo_id == voo_id, Reserva.status.in_(STATUS_OCUPA_ASSENTO))
            .count()
        )
