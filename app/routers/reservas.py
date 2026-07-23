from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas, services
from app.database import get_db

router = APIRouter(prefix="/reservas", tags=["reservas"])


def _verificar_disponibilidade(db: Session, voo: models.Voo):
    ocupados = services.contar_assentos_ocupados(db, voo.id)
    if ocupados >= voo.aeronave.capacidade_maxima:
        raise HTTPException(status_code=400, detail="Voo sem assentos disponíveis")


@router.get("/", response_model=list[schemas.ReservaRead])
def listar_reservas(db: Session = Depends(get_db)):
    return db.query(models.Reserva).all()


@router.post("/", response_model=schemas.ReservaRead, status_code=201)
def criar_reserva(reserva: schemas.ReservaCreate, db: Session = Depends(get_db)):
    voo = db.get(models.Voo, reserva.voo_id)
    if not voo:
        raise HTTPException(status_code=404, detail="Voo não encontrado")
    if not db.get(models.Passageiro, reserva.passageiro_id):
        raise HTTPException(status_code=404, detail="Passageiro não encontrado")

    existente = (
        db.query(models.Reserva)
        .filter(
            models.Reserva.passageiro_id == reserva.passageiro_id,
            models.Reserva.voo_id == reserva.voo_id,
        )
        .first()
    )
    if existente:
        raise HTTPException(
            status_code=409, detail="Passageiro já possui reserva neste voo"
        )

    _verificar_disponibilidade(db, voo)

    nova = models.Reserva(**reserva.model_dump())
    db.add(nova)
    db.commit()
    db.refresh(nova)
    return nova


@router.get("/{reserva_id}", response_model=schemas.ReservaRead)
def obter_reserva(reserva_id: int, db: Session = Depends(get_db)):
    reserva = db.get(models.Reserva, reserva_id)
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva não encontrada")
    return reserva


@router.patch("/{reserva_id}", response_model=schemas.ReservaRead)
def atualizar_reserva(
    reserva_id: int, dados: schemas.ReservaUpdate, db: Session = Depends(get_db)
):
    reserva = db.get(models.Reserva, reserva_id)
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva não encontrada")
    for campo, valor in dados.model_dump(exclude_unset=True).items():
        setattr(reserva, campo, valor)
    db.commit()
    db.refresh(reserva)
    return reserva


@router.delete("/{reserva_id}", status_code=204)
def deletar_reserva(reserva_id: int, db: Session = Depends(get_db)):
    reserva = db.get(models.Reserva, reserva_id)
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva não encontrada")
    db.delete(reserva)
    db.commit()


@router.post("/{reserva_id}/realocar", response_model=schemas.ReservaRead, status_code=201)
def realocar_reserva(
    reserva_id: int, dados: schemas.ReservaRealocar, db: Session = Depends(get_db)
):
    reserva_original = db.get(models.Reserva, reserva_id)
    if not reserva_original:
        raise HTTPException(status_code=404, detail="Reserva não encontrada")

    novo_voo = db.get(models.Voo, dados.novo_voo_id)
    if not novo_voo:
        raise HTTPException(status_code=404, detail="Voo de destino não encontrado")

    existente = (
        db.query(models.Reserva)
        .filter(
            models.Reserva.passageiro_id == reserva_original.passageiro_id,
            models.Reserva.voo_id == dados.novo_voo_id,
        )
        .first()
    )
    if existente:
        raise HTTPException(
            status_code=409, detail="Passageiro já possui reserva no voo de destino"
        )

    _verificar_disponibilidade(db, novo_voo)

    reserva_original.status = "realocado"

    nova_reserva = models.Reserva(
        passageiro_id=reserva_original.passageiro_id,
        voo_id=dados.novo_voo_id,
        status="confirmado",
        realocado_de_reserva_id=reserva_original.id,
    )
    db.add(nova_reserva)
    db.commit()
    db.refresh(nova_reserva)
    return nova_reserva
