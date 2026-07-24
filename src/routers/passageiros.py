from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database.database import get_db
from src.models import passageiro_model
from src.repositories.passageiro_repository import PassageiroRepository
from src.use_cases.passageiro import passageiro_use_cases

router = APIRouter(prefix="/passageiros", tags=["passageiros"])


@router.get("/", response_model=list[passageiro_model.PassageiroRead])
def listar_passageiros(db: Session = Depends(get_db)):
    return passageiro_use_cases.list_passageiros(PassageiroRepository(db))


@router.post("/", response_model=passageiro_model.PassageiroRead, status_code=201)
def criar_passageiro(dados: passageiro_model.PassageiroCreate, db: Session = Depends(get_db)):
    return passageiro_use_cases.create_passageiro(PassageiroRepository(db), dados)


@router.get("/{passageiro_id}", response_model=passageiro_model.PassageiroRead)
def obter_passageiro(passageiro_id: int, db: Session = Depends(get_db)):
    return passageiro_use_cases.get_passageiro(PassageiroRepository(db), passageiro_id)


@router.put("/{passageiro_id}", response_model=passageiro_model.PassageiroRead)
def atualizar_passageiro(
    passageiro_id: int, dados: passageiro_model.PassageiroCreate, db: Session = Depends(get_db)
):
    return passageiro_use_cases.update_passageiro(PassageiroRepository(db), passageiro_id, dados)


@router.delete("/{passageiro_id}", status_code=204)
def deletar_passageiro(passageiro_id: int, db: Session = Depends(get_db)):
    passageiro_use_cases.delete_passageiro(PassageiroRepository(db), passageiro_id)
