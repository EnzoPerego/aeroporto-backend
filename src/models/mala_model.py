from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict

StatusMala = Literal["despachada", "em_triagem", "carregada", "extraviada", "entregue"]


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
