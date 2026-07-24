from src.entities.aeronave import Aeronave
from src.repositories.base_repository import BaseRepository


class AeronaveRepository(BaseRepository[Aeronave]):
    model = Aeronave
