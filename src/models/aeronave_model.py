from pydantic import BaseModel, ConfigDict


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
