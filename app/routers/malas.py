from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/malas", tags=["malas"])


@router.get("/", response_model=list[schemas.MalaRead])
def listar_malas(db: Session = Depends(get_db)):
    return db.query(models.Mala).all()


@router.post("/", response_model=schemas.MalaRead, status_code=201)
def criar_mala(mala: schemas.MalaCreate, db: Session = Depends(get_db)):
    if not db.get(models.Reserva, mala.reserva_id):
        raise HTTPException(status_code=404, detail="Reserva não encontrada")
    nova = models.Mala(**mala.model_dump())
    db.add(nova)
    db.commit()
    db.refresh(nova)
    return nova


@router.get("/{mala_id}", response_model=schemas.MalaRead)
def obter_mala(mala_id: int, db: Session = Depends(get_db)):
    mala = db.get(models.Mala, mala_id)
    if not mala:
        raise HTTPException(status_code=404, detail="Mala não encontrada")
    return mala


@router.patch("/{mala_id}", response_model=schemas.MalaRead)
def atualizar_mala(mala_id: int, dados: schemas.MalaUpdate, db: Session = Depends(get_db)):
    mala = db.get(models.Mala, mala_id)
    if not mala:
        raise HTTPException(status_code=404, detail="Mala não encontrada")
    for campo, valor in dados.model_dump(exclude_unset=True).items():
        setattr(mala, campo, valor)
    db.commit()
    db.refresh(mala)
    return mala


@router.delete("/{mala_id}", status_code=204)
def deletar_mala(mala_id: int, db: Session = Depends(get_db)):
    mala = db.get(models.Mala, mala_id)
    if not mala:
        raise HTTPException(status_code=404, detail="Mala não encontrada")
    db.delete(mala)
    db.commit()
