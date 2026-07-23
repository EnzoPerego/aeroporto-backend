from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/terminais", tags=["terminais"])


@router.get("/", response_model=list[schemas.TerminalRead])
def listar_terminais(db: Session = Depends(get_db)):
    return db.query(models.Terminal).all()


@router.post("/", response_model=schemas.TerminalRead, status_code=201)
def criar_terminal(terminal: schemas.TerminalCreate, db: Session = Depends(get_db)):
    novo = models.Terminal(**terminal.model_dump())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo


@router.get("/{terminal_id}", response_model=schemas.TerminalRead)
def obter_terminal(terminal_id: int, db: Session = Depends(get_db)):
    terminal = db.get(models.Terminal, terminal_id)
    if not terminal:
        raise HTTPException(status_code=404, detail="Terminal não encontrado")
    return terminal


@router.put("/{terminal_id}", response_model=schemas.TerminalRead)
def atualizar_terminal(
    terminal_id: int, dados: schemas.TerminalCreate, db: Session = Depends(get_db)
):
    terminal = db.get(models.Terminal, terminal_id)
    if not terminal:
        raise HTTPException(status_code=404, detail="Terminal não encontrado")
    for campo, valor in dados.model_dump().items():
        setattr(terminal, campo, valor)
    db.commit()
    db.refresh(terminal)
    return terminal


@router.delete("/{terminal_id}", status_code=204)
def deletar_terminal(terminal_id: int, db: Session = Depends(get_db)):
    terminal = db.get(models.Terminal, terminal_id)
    if not terminal:
        raise HTTPException(status_code=404, detail="Terminal não encontrado")
    db.delete(terminal)
    db.commit()
