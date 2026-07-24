from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database.database import get_db
from src.models import gate_model
from src.repositories.gate_repository import GateRepository
from src.use_cases.gate import gate_use_cases

router = APIRouter(prefix="/gates", tags=["gates"])


@router.get("/", response_model=list[gate_model.GateRead])
def listar_gates(db: Session = Depends(get_db)):
    return gate_use_cases.list_gates(GateRepository(db))


@router.post("/", response_model=gate_model.GateRead, status_code=201)
def criar_gate(dados: gate_model.GateCreate, db: Session = Depends(get_db)):
    return gate_use_cases.create_gate(GateRepository(db), dados)


@router.get("/{gate_id}", response_model=gate_model.GateRead)
def obter_gate(gate_id: int, db: Session = Depends(get_db)):
    return gate_use_cases.get_gate(GateRepository(db), gate_id)


@router.patch("/{gate_id}", response_model=gate_model.GateRead)
def atualizar_gate(gate_id: int, dados: gate_model.GateUpdate, db: Session = Depends(get_db)):
    return gate_use_cases.update_gate(GateRepository(db), gate_id, dados)


@router.delete("/{gate_id}", status_code=204)
def deletar_gate(gate_id: int, db: Session = Depends(get_db)):
    gate_use_cases.delete_gate(GateRepository(db), gate_id)
