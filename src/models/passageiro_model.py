from typing import Optional

from pydantic import BaseModel, ConfigDict


class PassageiroBase(BaseModel):
    nome: str
    documento: str
    email: Optional[str] = None


class PassageiroCreate(PassageiroBase):
    pass


class PassageiroRead(PassageiroBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
