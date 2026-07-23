from sqlalchemy import CheckConstraint, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Aeronave(Base):
    __tablename__ = "aeronaves"

    id: Mapped[int] = mapped_column(primary_key=True)
    modelo: Mapped[str] = mapped_column(String(100), nullable=False)
    matricula: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    capacidade_maxima: Mapped[int] = mapped_column(
        Integer, CheckConstraint("capacidade_maxima > 0"), nullable=False
    )

    voos: Mapped[list["Voo"]] = relationship(back_populates="aeronave")
