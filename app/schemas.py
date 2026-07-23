from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict

TipoTerminal = Literal["nacional", "internacional"]
StatusGate = Literal["livre", "ocupado"]
StatusVoo = Literal["no_horario", "atrasado", "embarcando", "finalizado", "cancelado"]
StatusReserva = Literal["confirmado", "checkin_feito", "embarcado", "perdeu_voo", "realocado"]
StatusMala = Literal["despachada", "em_triagem", "carregada", "extraviada", "entregue"]


# ---------------------------------------------------------------------
# Terminal
# ---------------------------------------------------------------------
class TerminalBase(BaseModel):
    nome: str
    tipo: TipoTerminal


class TerminalCreate(TerminalBase):
    pass


class TerminalRead(TerminalBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


# ---------------------------------------------------------------------
# Gate
# ---------------------------------------------------------------------
class GateBase(BaseModel):
    codigo: str
    terminal_id: int
    status: StatusGate = "livre"


class GateCreate(GateBase):
    pass


class GateUpdate(BaseModel):
    codigo: Optional[str] = None
    terminal_id: Optional[int] = None
    status: Optional[StatusGate] = None


class GateRead(GateBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


# ---------------------------------------------------------------------
# Aeronave
# ---------------------------------------------------------------------
class AeronaveBase(BaseModel):
    modelo: str
    matricula: str
    capacidade_maxima: int


class AeronaveCreate(AeronaveBase):
    pass


class AeronaveRead(AeronaveBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class AeronaveOcupacao(BaseModel):
    aeronave_id: int
    capacidade_maxima: int
    assentos_ocupados: int
    assentos_disponiveis: int


# ---------------------------------------------------------------------
# Voo
# ---------------------------------------------------------------------
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


# ---------------------------------------------------------------------
# Passageiro
# ---------------------------------------------------------------------
class PassageiroBase(BaseModel):
    nome: str
    documento: str
    email: Optional[str] = None


class PassageiroCreate(PassageiroBase):
    pass


class PassageiroRead(PassageiroBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


# ---------------------------------------------------------------------
# Reserva
# ---------------------------------------------------------------------
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


# ---------------------------------------------------------------------
# Mala
# ---------------------------------------------------------------------
class MalaBase(BaseModel):
    codigo_identificacao: str
    reserva_id: int
    status: StatusMala = "despachada"
    localizacao_atual: Optional[str] = None


class MalaCreate(MalaBase):
    pass


class MalaUpdate(BaseModel):
    status: Optional[StatusMala] = None
    localizacao_atual: Optional[str] = None


class MalaRead(MalaBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
