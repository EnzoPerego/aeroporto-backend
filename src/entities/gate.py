from sqlalchemy import Enum, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.database import Base

StatusGate = Enum("livre", "ocupado", name="status_gate")


class Gate(Base):
    __tablename__ = "gates"
    __table_args__ = (UniqueConstraint("terminal_id", "codigo"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    codigo: Mapped[str] = mapped_column(String(10), nullable=False)
    terminal_id: Mapped[int] = mapped_column(ForeignKey("terminais.id"), nullable=False)
    status: Mapped[str] = mapped_column(StatusGate, nullable=False, default="livre")

    terminal: Mapped["Terminal"] = relationship(back_populates="gates")
    voos: Mapped[list["Voo"]] = relationship(back_populates="gate")
