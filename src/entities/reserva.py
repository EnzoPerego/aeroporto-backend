from typing import Optional

from sqlalchemy import Enum, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.database import Base

StatusReserva = Enum(
    "confirmado", "checkin_feito", "embarcado", "perdeu_voo", "realocado",
    name="status_reserva",
)


class Reserva(Base):
    """Liga um passageiro a um voo especifico (resolve o N:N passageiro<->voo).

    Uma realocacao cria uma NOVA reserva referenciando a original via
    realocado_de_reserva_id, preservando o historico em vez de sobrescrever.
    """

    __tablename__ = "reservas"
    __table_args__ = (UniqueConstraint("passageiro_id", "voo_id"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    passageiro_id: Mapped[int] = mapped_column(ForeignKey("passageiros.id"), nullable=False)
    voo_id: Mapped[int] = mapped_column(ForeignKey("voos.id"), nullable=False)
    status: Mapped[str] = mapped_column(StatusReserva, nullable=False, default="confirmado")
    assento: Mapped[Optional[str]] = mapped_column(String(5), nullable=True)
    realocado_de_reserva_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("reservas.id"), nullable=True
    )

    passageiro: Mapped["Passageiro"] = relationship(back_populates="reservas")
    voo: Mapped["Voo"] = relationship(back_populates="reservas")
    malas: Mapped[list["Mala"]] = relationship(
        back_populates="reserva", cascade="all, delete-orphan"
    )
