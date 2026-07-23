from typing import Optional

from sqlalchemy.orm import Session

from app import models

STATUS_OCUPA_ASSENTO = ("confirmado", "checkin_feito", "embarcado")


def contar_assentos_ocupados(db: Session, voo_id: int) -> int:
    return (
        db.query(models.Reserva)
        .filter(
            models.Reserva.voo_id == voo_id,
            models.Reserva.status.in_(STATUS_OCUPA_ASSENTO),
        )
        .count()
    )


def voo_ativo_da_aeronave(db: Session, aeronave_id: int) -> Optional[models.Voo]:
    """Retorna o próximo voo não finalizado/cancelado associado à aeronave."""
    return (
        db.query(models.Voo)
        .filter(
            models.Voo.aeronave_id == aeronave_id,
            models.Voo.status.notin_(("finalizado", "cancelado")),
        )
        .order_by(models.Voo.horario_previsto_partida.asc())
        .first()
    )
