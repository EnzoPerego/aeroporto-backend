from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.database import Base

StatusVoo = Enum(
    "no_horario", "atrasado", "embarcando", "finalizado", "cancelado",
    name="status_voo",
)


class Voo(Base):
    __tablename__ = "voos"

    id: Mapped[int] = mapped_column(primary_key=True)
    numero_voo: Mapped[str] = mapped_column(String(10), nullable=False, unique=True)
    origem: Mapped[str] = mapped_column(String(100), nullable=False)
    destino: Mapped[str] = mapped_column(String(100), nullable=False)
    horario_previsto_chegada: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    horario_previsto_partida: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    status: Mapped[str] = mapped_column(StatusVoo, nullable=False, default="no_horario")
    aeronave_id: Mapped[int] = mapped_column(ForeignKey("aeronaves.id"), nullable=False)
    terminal_id: Mapped[int] = mapped_column(ForeignKey("terminais.id"), nullable=False)
    gate_id: Mapped[Optional[int]] = mapped_column(ForeignKey("gates.id"), nullable=True)

    aeronave: Mapped["Aeronave"] = relationship(back_populates="voos")
    terminal: Mapped["Terminal"] = relationship(back_populates="voos")
    gate: Mapped[Optional["Gate"]] = relationship(back_populates="voos")
    reservas: Mapped[list["Reserva"]] = relationship(back_populates="voo")
