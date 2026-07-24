from fastapi import HTTPException

from src.entities.gate import Gate
from src.models.gate_model import GateCreate, GateUpdate
from src.repositories.gate_repository import GateRepository


def list_gates(repo: GateRepository) -> list[Gate]:
    return repo.list_all()


def get_gate(repo: GateRepository, gate_id: int) -> Gate:
    gate = repo.get(gate_id)
    if not gate:
        raise HTTPException(status_code=404, detail="Gate não encontrado")
    return gate


def create_gate(repo: GateRepository, dados: GateCreate) -> Gate:
    return repo.create(**dados.model_dump())


def update_gate(repo: GateRepository, gate_id: int, dados: GateUpdate) -> Gate:
    gate = get_gate(repo, gate_id)
    return repo.update(gate, **dados.model_dump(exclude_unset=True))


def delete_gate(repo: GateRepository, gate_id: int) -> None:
    gate = get_gate(repo, gate_id)
    repo.delete(gate)
