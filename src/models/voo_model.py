from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict

StatusVoo = Literal["no_horario", "atrasado", "embarcando", "finalizado", "cancelado"]


class VooBase(BaseModel):
    numero_voo: str
    origem: str
    destino: str
    horario_previsto_chegada: Optional[datetime] = None
    horario_previsto_partida: Optional[datetime] = None
    status: StatusVoo = "no_horario"
    aeronave_id: int
    terminal_id: int
    gate_id: Optional[int] = None


class VooCreate(VooBase):
    pass


class VooUpdate(BaseModel):
    numero_voo: Optional[str] = None
    origem: Optional[str] = None
    destino: Optional[str] = None
    horario_previsto_chegada: Optional[datetime] = None
    horario_previsto_partida: Optional[datetime] = None
    status: Optional[StatusVoo] = None
    aeronave_id: Optional[int] = None
    terminal_id: Optional[int] = None
    gate_id: Optional[int] = None


class VooRead(VooBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
