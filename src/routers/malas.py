from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database.database import get_db
from src.models import mala_model
from src.repositories.mala_repository import MalaRepository
from src.repositories.reserva_repository import ReservaRepository
from src.use_cases.mala import mala_use_cases

router = APIRouter(prefix="/malas", tags=["malas"])


@router.get("/", response_model=list[mala_model.MalaRead])
def listar_malas(db: Session = Depends(get_db)):
    return mala_use_cases.list_malas(MalaRepository(db))


@router.post("/", response_model=mala_model.MalaRead, status_code=201)
def criar_mala(dados: mala_model.MalaCreate, db: Session = Depends(get_db)):
    return mala_use_cases.create_mala(MalaRepository(db), ReservaRepository(db), dados)


@router.get("/{mala_id}", response_model=mala_model.MalaRead)
def obter_mala(mala_id: int, db: Session = Depends(get_db)):
    return mala_use_cases.get_mala(MalaRepository(db), mala_id)


@router.patch("/{mala_id}", response_model=mala_model.MalaRead)
def atualizar_mala(mala_id: int, dados: mala_model.MalaUpdate, db: Session = Depends(get_db)):
    return mala_use_cases.update_mala(MalaRepository(db), mala_id, dados)


@router.delete("/{mala_id}", status_code=204)
def deletar_mala(mala_id: int, db: Session = Depends(get_db)):
    mala_use_cases.delete_mala(MalaRepository(db), mala_id)
