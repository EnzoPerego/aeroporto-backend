from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/gates", tags=["gates"])


@router.get("/", response_model=list[schemas.GateRead])
def listar_gates(db: Session = Depends(get_db)):
    return db.query(models.Gate).all()


@router.post("/", response_model=schemas.GateRead, status_code=201)
def criar_gate(gate: schemas.GateCreate, db: Session = Depends(get_db)):
    novo = models.Gate(**gate.model_dump())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo


@router.get("/{gate_id}", response_model=schemas.GateRead)
def obter_gate(gate_id: int, db: Session = Depends(get_db)):
    gate = db.get(models.Gate, gate_id)
    if not gate:
        raise HTTPException(status_code=404, detail="Gate não encontrado")
    return gate


@router.patch("/{gate_id}", response_model=schemas.GateRead)
def atualizar_gate(gate_id: int, dados: schemas.GateUpdate, db: Session = Depends(get_db)):
    gate = db.get(models.Gate, gate_id)
    if not gate:
        raise HTTPException(status_code=404, detail="Gate não encontrado")
    for campo, valor in dados.model_dump(exclude_unset=True).items():
        setattr(gate, campo, valor)
    db.commit()
    db.refresh(gate)
    return gate


@router.delete("/{gate_id}", status_code=204)
def deletar_gate(gate_id: int, db: Session = Depends(get_db)):
    gate = db.get(models.Gate, gate_id)
    if not gate:
        raise HTTPException(status_code=404, detail="Gate não encontrado")
    db.delete(gate)
    db.commit()
