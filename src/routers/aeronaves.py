from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database.database import get_db
from src.models import aeronave_model
from src.repositories.aeronave_repository import AeronaveRepository
from src.repositories.reserva_repository import ReservaRepository
from src.repositories.voo_repository import VooRepository
from src.use_cases.aeronave import aeronave_use_cases

router = APIRouter(prefix="/aeronaves", tags=["aeronaves"])


@router.get("/", response_model=list[aeronave_model.AeronaveRead])
def listar_aeronaves(db: Session = Depends(get_db)):
    return aeronave_use_cases.list_aeronaves(AeronaveRepository(db))


@router.post("/", response_model=aeronave_model.AeronaveRead, status_code=201)
def criar_aeronave(dados: aeronave_model.AeronaveCreate, db: Session = Depends(get_db)):
    return aeronave_use_cases.create_aeronave(AeronaveRepository(db), dados)


@router.get("/{aeronave_id}", response_model=aeronave_model.AeronaveRead)
def obter_aeronave(aeronave_id: int, db: Session = Depends(get_db)):
    return aeronave_use_cases.get_aeronave(AeronaveRepository(db), aeronave_id)


@router.put("/{aeronave_id}", response_model=aeronave_model.AeronaveRead)
def atualizar_aeronave(
    aeronave_id: int, dados: aeronave_model.AeronaveCreate, db: Session = Depends(get_db)
):
    return aeronave_use_cases.update_aeronave(AeronaveRepository(db), aeronave_id, dados)


@router.delete("/{aeronave_id}", status_code=204)
def deletar_aeronave(aeronave_id: int, db: Session = Depends(get_db)):
    aeronave_use_cases.delete_aeronave(AeronaveRepository(db), aeronave_id)


@router.get("/{aeronave_id}/ocupacao", response_model=aeronave_model.AeronaveOcupacao)
def ocupacao_aeronave(aeronave_id: int, db: Session = Depends(get_db)):
    return aeronave_use_cases.get_ocupacao_aeronave(
        AeronaveRepository(db), VooRepository(db), ReservaRepository(db), aeronave_id
    )
