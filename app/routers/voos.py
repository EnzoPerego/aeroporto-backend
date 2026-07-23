from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas, services
from app.database import get_db

router = APIRouter(prefix="/voos", tags=["voos"])


@router.get("/", response_model=list[schemas.VooRead])
def listar_voos(db: Session = Depends(get_db)):
    return db.query(models.Voo).all()


@router.post("/", response_model=schemas.VooRead, status_code=201)
def criar_voo(voo: schemas.VooCreate, db: Session = Depends(get_db)):
    novo = models.Voo(**voo.model_dump())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo


@router.get("/{voo_id}", response_model=schemas.VooRead)
def obter_voo(voo_id: int, db: Session = Depends(get_db)):
    voo = db.get(models.Voo, voo_id)
    if not voo:
        raise HTTPException(status_code=404, detail="Voo não encontrado")
    return voo


@router.patch("/{voo_id}", response_model=schemas.VooRead)
def atualizar_voo(voo_id: int, dados: schemas.VooUpdate, db: Session = Depends(get_db)):
    voo = db.get(models.Voo, voo_id)
    if not voo:
        raise HTTPException(status_code=404, detail="Voo não encontrado")
    for campo, valor in dados.model_dump(exclude_unset=True).items():
        setattr(voo, campo, valor)
    db.commit()
    db.refresh(voo)
    return voo


@router.delete("/{voo_id}", status_code=204)
def deletar_voo(voo_id: int, db: Session = Depends(get_db)):
    voo = db.get(models.Voo, voo_id)
    if not voo:
        raise HTTPException(status_code=404, detail="Voo não encontrado")
    db.delete(voo)
    db.commit()


@router.get("/{voo_id}/passageiros", response_model=list[schemas.ReservaComPassageiro])
def passageiros_do_voo(voo_id: int, db: Session = Depends(get_db)):
    voo = db.get(models.Voo, voo_id)
    if not voo:
        raise HTTPException(status_code=404, detail="Voo não encontrado")
    return db.query(models.Reserva).filter(models.Reserva.voo_id == voo_id).all()


@router.get("/{voo_id}/ocupacao", response_model=schemas.AeronaveOcupacao)
def ocupacao_voo(voo_id: int, db: Session = Depends(get_db)):
    voo = db.get(models.Voo, voo_id)
    if not voo:
        raise HTTPException(status_code=404, detail="Voo não encontrado")
    ocupados = services.contar_assentos_ocupados(db, voo_id)
    return schemas.AeronaveOcupacao(
        aeronave_id=voo.aeronave_id,
        capacidade_maxima=voo.aeronave.capacidade_maxima,
        assentos_ocupados=ocupados,
        assentos_disponiveis=voo.aeronave.capacidade_maxima - ocupados,
    )
