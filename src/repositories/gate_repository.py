from src.entities.gate import Gate
from src.repositories.base_repository import BaseRepository


class GateRepository(BaseRepository[Gate]):
    model = Gate
