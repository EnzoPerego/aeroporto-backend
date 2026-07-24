from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict

StatusGate = Literal["livre", "ocupado"]


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
