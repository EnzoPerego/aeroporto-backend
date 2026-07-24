from typing import Literal

from pydantic import BaseModel, ConfigDict

TipoTerminal = Literal["nacional", "internacional"]


class TerminalBase(BaseModel):
    nome: str
    tipo: TipoTerminal


class TerminalCreate(TerminalBase):
    pass


class TerminalRead(TerminalBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
