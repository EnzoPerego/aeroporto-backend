from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database.database import get_db
from src.models import aeronave_model, reserva_model, voo_model
from src.repositories.reserva_repository import ReservaRepository
from src.repositories.voo_repository import VooRepository
from src.use_cases.voo.create_voo import create_voo
from src.use_cases.voo.delete_voo import delete_voo
from src.use_cases.voo.get_ocupacao_voo import get_ocupacao_voo
from src.use_cases.voo.get_voo import get_voo
from src.use_cases.voo.list_passageiros_do_voo import list_passageiros_do_voo
from src.use_cases.voo.list_voos import list_voos
from src.use_cases.voo.update_voo import update_voo

router = APIRouter(prefix="/voos", tags=["voos"])


@router.get("/", response_model=list[voo_model.VooRead])
def listar_voos(db: Session = Depends(get_db)):
    return list_voos(VooRepository(db))


@router.post("/", response_model=voo_model.VooRead, status_code=201)
def criar_voo(dados: voo_model.VooCreate, db: Session = Depends(get_db)):
    return create_voo(VooRepository(db), dados)


@router.get("/{voo_id}", response_model=voo_model.VooRead)
def obter_voo(voo_id: int, db: Session = Depends(get_db)):
    return get_voo(VooRepository(db), voo_id)


@router.patch("/{voo_id}", response_model=voo_model.VooRead)
def atualizar_voo(voo_id: int, dados: voo_model.VooUpdate, db: Session = Depends(get_db)):
    return update_voo(VooRepository(db), voo_id, dados)


@router.delete("/{voo_id}", status_code=204)
def deletar_voo(voo_id: int, db: Session = Depends(get_db)):
    delete_voo(VooRepository(db), voo_id)


@router.get("/{voo_id}/passageiros", response_model=list[reserva_model.ReservaComPassageiro])
def passageiros_do_voo(voo_id: int, db: Session = Depends(get_db)):
    return list_passageiros_do_voo(VooRepository(db), ReservaRepository(db), voo_id)


@router.get("/{voo_id}/ocupacao", response_model=aeronave_model.AeronaveOcupacao)
def ocupacao_voo(voo_id: int, db: Session = Depends(get_db)):
    return get_ocupacao_voo(VooRepository(db), ReservaRepository(db), voo_id)
