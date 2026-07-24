from src.entities.mala import Mala
from src.repositories.base_repository import BaseRepository


class MalaRepository(BaseRepository[Mala]):
    model = Mala
