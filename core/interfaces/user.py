from abc import ABC, abstractmethod
from typing import Optional

class IUserRepo(ABC):
    @abstractmethod
    async def save(self, user) -> None:
        pass

    @abstractmethod
    async def find_by_tg_id(self, telegram_id: str) -> Optional['User']:
        pass