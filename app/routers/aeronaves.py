from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas, services
from app.database import get_db

router = APIRouter(prefix="/aeronaves", tags=["aeronaves"])


@router.get("/", response_model=list[schemas.AeronaveRead])
def listar_aeronaves(db: Session = Depends(get_db)):
    return db.query(models.Aeronave).all()


@router.post("/", response_model=schemas.AeronaveRead, status_code=201)
def criar_aeronave(aeronave: schemas.AeronaveCreate, db: Session = Depends(get_db)):
    nova = models.Aeronave(**aeronave.model_dump())
    db.add(nova)
    db.commit()
    db.refresh(nova)
    return nova


@router.get("/{aeronave_id}", response_model=schemas.AeronaveRead)
def obter_aeronave(aeronave_id: int, db: Session = Depends(get_db)):
    aeronave = db.get(models.Aeronave, aeronave_id)
    if not aeronave:
        raise HTTPException(status_code=404, detail="Aeronave não encontrada")
    return aeronave


@router.put("/{aeronave_id}", response_model=schemas.AeronaveRead)
def atualizar_aeronave(
    aeronave_id: int, dados: schemas.AeronaveCreate, db: Session = Depends(get_db)
):
    aeronave = db.get(models.Aeronave, aeronave_id)
    if not aeronave:
        raise HTTPException(status_code=404, detail="Aeronave não encontrada")
    for campo, valor in dados.model_dump().items():
        setattr(aeronave, campo, valor)
    db.commit()
    db.refresh(aeronave)
    return aeronave


@router.delete("/{aeronave_id}", status_code=204)
def deletar_aeronave(aeronave_id: int, db: Session = Depends(get_db)):
    aeronave = db.get(models.Aeronave, aeronave_id)
    if not aeronave:
        raise HTTPException(status_code=404, detail="Aeronave não encontrada")
    db.delete(aeronave)
    db.commit()


@router.get("/{aeronave_id}/ocupacao", response_model=schemas.AeronaveOcupacao)
def ocupacao_aeronave(aeronave_id: int, db: Session = Depends(get_db)):
    aeronave = db.get(models.Aeronave, aeronave_id)
    if not aeronave:
        raise HTTPException(status_code=404, detail="Aeronave não encontrada")

    voo = services.voo_ativo_da_aeronave(db, aeronave_id)
    ocupados = services.contar_assentos_ocupados(db, voo.id) if voo else 0

    return schemas.AeronaveOcupacao(
        aeronave_id=aeronave.id,
        capacidade_maxima=aeronave.capacidade_maxima,
        assentos_ocupados=ocupados,
        assentos_disponiveis=aeronave.capacidade_maxima - ocupados,
    )
