from src.entities.terminal import Terminal
from src.repositories.base_repository import BaseRepository


class TerminalRepository(BaseRepository[Terminal]):
    model = Terminal
