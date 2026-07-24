from src.entities.passageiro import Passageiro
from src.repositories.base_repository import BaseRepository


class PassageiroRepository(BaseRepository[Passageiro]):
    model = Passageiro
