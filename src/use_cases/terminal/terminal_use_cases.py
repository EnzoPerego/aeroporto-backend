from fastapi import HTTPException

from src.entities.terminal import Terminal
from src.models.terminal_model import TerminalCreate
from src.repositories.terminal_repository import TerminalRepository


def list_terminais(repo: TerminalRepository) -> list[Terminal]:
    return repo.list_all()


def get_terminal(repo: TerminalRepository, terminal_id: int) -> Terminal:
    terminal = repo.get(terminal_id)
    if not terminal:
        raise HTTPException(status_code=404, detail="Terminal não encontrado")
    return terminal


def create_terminal(repo: TerminalRepository, dados: TerminalCreate) -> Terminal:
    return repo.create(**dados.model_dump())


def update_terminal(repo: TerminalRepository, terminal_id: int, dados: TerminalCreate) -> Terminal:
    terminal = get_terminal(repo, terminal_id)
    return repo.update(terminal, **dados.model_dump())


def delete_terminal(repo: TerminalRepository, terminal_id: int) -> None:
    terminal = get_terminal(repo, terminal_id)
    repo.delete(terminal)
