from sqlalchemy import Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.database import Base

TipoTerminal = Enum("nacional", "internacional", name="tipo_terminal")


class Terminal(Base):
    __tablename__ = "terminais"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    tipo: Mapped[str] = mapped_column(TipoTerminal, nullable=False)

    gates: Mapped[list["Gate"]] = relationship(back_populates="terminal")
    voos: Mapped[list["Voo"]] = relationship(back_populates="terminal")
