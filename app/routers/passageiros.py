from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/passageiros", tags=["passageiros"])


@router.get("/", response_model=list[schemas.PassageiroRead])
def listar_passageiros(db: Session = Depends(get_db)):
    return db.query(models.Passageiro).all()


@router.post("/", response_model=schemas.PassageiroRead, status_code=201)
def criar_passageiro(passageiro: schemas.PassageiroCreate, db: Session = Depends(get_db)):
    novo = models.Passageiro(**passageiro.model_dump())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo


@router.get("/{passageiro_id}", response_model=schemas.PassageiroRead)
def obter_passageiro(passageiro_id: int, db: Session = Depends(get_db)):
    passageiro = db.get(models.Passageiro, passageiro_id)
    if not passageiro:
        raise HTTPException(status_code=404, detail="Passageiro não encontrado")
    return passageiro


@router.put("/{passageiro_id}", response_model=schemas.PassageiroRead)
def atualizar_passageiro(
    passageiro_id: int, dados: schemas.PassageiroCreate, db: Session = Depends(get_db)
):
    passageiro = db.get(models.Passageiro, passageiro_id)
    if not passageiro:
        raise HTTPException(status_code=404, detail="Passageiro não encontrado")
    for campo, valor in dados.model_dump().items():
        setattr(passageiro, campo, valor)
    db.commit()
    db.refresh(passageiro)
    return passageiro


@router.delete("/{passageiro_id}", status_code=204)
def deletar_passageiro(passageiro_id: int, db: Session = Depends(get_db)):
    passageiro = db.get(models.Passageiro, passageiro_id)
    if not passageiro:
        raise HTTPException(status_code=404, detail="Passageiro não encontrado")
    db.delete(passageiro)
    db.commit()
