from abc import ABC, abstractmethod
from typing import Optional, List

from core.models.user import User

class IUserRepo(ABC):
    @abstractmethod
    async def save(self, user) -> None:
        pass

    @abstractmethod
    async def find_by_tg_id(self, telegram_id: str) -> Optional['User']:
        pass
    
    @abstractmethod
    async def find_all(self) -> Optional[List['User']]:
        pass