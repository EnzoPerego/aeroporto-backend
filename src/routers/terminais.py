from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database.database import get_db
from src.models import terminal_model
from src.repositories.terminal_repository import TerminalRepository
from src.use_cases.terminal import terminal_use_cases

router = APIRouter(prefix="/terminais", tags=["terminais"])


@router.get("/", response_model=list[terminal_model.TerminalRead])
def listar_terminais(db: Session = Depends(get_db)):
    return terminal_use_cases.list_terminais(TerminalRepository(db))


@router.post("/", response_model=terminal_model.TerminalRead, status_code=201)
def criar_terminal(dados: terminal_model.TerminalCreate, db: Session = Depends(get_db)):
    return terminal_use_cases.create_terminal(TerminalRepository(db), dados)


@router.get("/{terminal_id}", response_model=terminal_model.TerminalRead)
def obter_terminal(terminal_id: int, db: Session = Depends(get_db)):
    return terminal_use_cases.get_terminal(TerminalRepository(db), terminal_id)


@router.put("/{terminal_id}", response_model=terminal_model.TerminalRead)
def atualizar_terminal(
    terminal_id: int, dados: terminal_model.TerminalCreate, db: Session = Depends(get_db)
):
    return terminal_use_cases.update_terminal(TerminalRepository(db), terminal_id, dados)


@router.delete("/{terminal_id}", status_code=204)
def deletar_terminal(terminal_id: int, db: Session = Depends(get_db)):
    terminal_use_cases.delete_terminal(TerminalRepository(db), terminal_id)
