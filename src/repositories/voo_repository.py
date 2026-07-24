from typing import Optional

from src.entities.voo import Voo
from src.repositories.base_repository import BaseRepository

STATUS_VOO_ATIVOS_EXCLUIDOS = ("finalizado", "cancelado")


class VooRepository(BaseRepository[Voo]):
    model = Voo

    def find_ativo_por_aeronave(self, aeronave_id: int) -> Optional[Voo]:
        """Proximo voo nao finalizado/cancelado associado a aeronave."""
        return (
            self.db.query(Voo)
            .filter(
                Voo.aeronave_id == aeronave_id,
                Voo.status.notin_(STATUS_VOO_ATIVOS_EXCLUIDOS),
            )
            .order_by(Voo.horario_previsto_partida.asc())
            .first()
        )
