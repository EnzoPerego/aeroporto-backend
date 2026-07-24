from fastapi import HTTPException

from src.entities.reserva import Reserva
from src.models.reserva_model import ReservaRealocar
from src.repositories.reserva_repository import ReservaRepository
from src.repositories.voo_repository import VooRepository
from src.use_cases.reserva.get_reserva import get_reserva


def realocar_reserva(
    reserva_repo: ReservaRepository,
    voo_repo: VooRepository,
    reserva_id: int,
    dados: ReservaRealocar,
) -> Reserva:
    reserva_original = get_reserva(reserva_repo, reserva_id)

    novo_voo = voo_repo.get(dados.novo_voo_id)
    if not novo_voo:
        raise HTTPException(status_code=404, detail="Voo de destino não encontrado")

    if reserva_repo.find_by_passageiro_e_voo(reserva_original.passageiro_id, dados.novo_voo_id):
        raise HTTPException(
            status_code=409, detail="Passageiro já possui reserva no voo de destino"
        )

    ocupados = reserva_repo.contar_assentos_ocupados(novo_voo.id)
    if ocupados >= novo_voo.aeronave.capacidade_maxima:
        raise HTTPException(status_code=400, detail="Voo sem assentos disponíveis")

    reserva_repo.update(reserva_original, status="realocado")

    return reserva_repo.create(
        passageiro_id=reserva_original.passageiro_id,
        voo_id=dados.novo_voo_id,
        status="confirmado",
        realocado_de_reserva_id=reserva_original.id,
    )
