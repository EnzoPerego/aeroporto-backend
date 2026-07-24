from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict

from src.models.passageiro_model import PassageiroRead

StatusReserva = Literal["confirmado", "checkin_feito", "embarcado", "perdeu_voo", "realocado"]


class ReservaBase(BaseModel):
    passageiro_id: int
    voo_id: int
    assento: Optional[str] = None


class ReservaCreate(ReservaBase):
    pass


class ReservaUpdate(BaseModel):
    status: Optional[StatusReserva] = None
    assento: Optional[str] = None


class ReservaRealocar(BaseModel):
    novo_voo_id: int


class ReservaRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    passageiro_id: int
    voo_id: int
    status: StatusReserva
    assento: Optional[str] = None
    realocado_de_reserva_id: Optional[int] = None


class ReservaComPassageiro(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    status: StatusReserva
    assento: Optional[str] = None
    passageiro: PassageiroRead
