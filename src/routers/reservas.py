from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database.database import get_db
from src.models import reserva_model
from src.repositories.passageiro_repository import PassageiroRepository
from src.repositories.reserva_repository import ReservaRepository
from src.repositories.voo_repository import VooRepository
from src.use_cases.reserva.create_reserva import create_reserva
from src.use_cases.reserva.delete_reserva import delete_reserva
from src.use_cases.reserva.get_reserva import get_reserva
from src.use_cases.reserva.list_reservas import list_reservas
from src.use_cases.reserva.realocar_reserva import realocar_reserva
from src.use_cases.reserva.update_reserva import update_reserva

router = APIRouter(prefix="/reservas", tags=["reservas"])


@router.get("/", response_model=list[reserva_model.ReservaRead])
def listar_reservas(db: Session = Depends(get_db)):
    return list_reservas(ReservaRepository(db))


@router.post("/", response_model=reserva_model.ReservaRead, status_code=201)
def criar_reserva(dados: reserva_model.ReservaCreate, db: Session = Depends(get_db)):
    return create_reserva(ReservaRepository(db), VooRepository(db), PassageiroRepository(db), dados)


@router.get("/{reserva_id}", response_model=reserva_model.ReservaRead)
def obter_reserva(reserva_id: int, db: Session = Depends(get_db)):
    return get_reserva(ReservaRepository(db), reserva_id)


@router.patch("/{reserva_id}", response_model=reserva_model.ReservaRead)
def atualizar_reserva(
    reserva_id: int, dados: reserva_model.ReservaUpdate, db: Session = Depends(get_db)
):
    return update_reserva(ReservaRepository(db), reserva_id, dados)


@router.delete("/{reserva_id}", status_code=204)
def deletar_reserva(reserva_id: int, db: Session = Depends(get_db)):
    delete_reserva(ReservaRepository(db), reserva_id)


@router.post("/{reserva_id}/realocar", response_model=reserva_model.ReservaRead, status_code=201)
def realocar(reserva_id: int, dados: reserva_model.ReservaRealocar, db: Session = Depends(get_db)):
    return realocar_reserva(ReservaRepository(db), VooRepository(db), reserva_id, dados)
