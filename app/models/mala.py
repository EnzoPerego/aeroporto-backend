from typing import Optional

from sqlalchemy import Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

StatusMala = Enum(
    "despachada", "em_triagem", "carregada", "extraviada", "entregue",
    name="status_mala",
)


class Mala(Base):
    """Mala despachada por um passageiro; ligada a reserva (passageiro+voo)."""

    __tablename__ = "malas"

    id: Mapped[int] = mapped_column(primary_key=True)
    codigo_identificacao: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    reserva_id: Mapped[int] = mapped_column(ForeignKey("reservas.id"), nullable=False)
    status: Mapped[str] = mapped_column(StatusMala, nullable=False, default="despachada")
    localizacao_atual: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    reserva: Mapped["Reserva"] = relationship(back_populates="malas")
