from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Passageiro(Base):
    __tablename__ = "passageiros"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(150), nullable=False)
    documento: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    email: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)

    reservas: Mapped[list["Reserva"]] = relationship(back_populates="passageiro")
