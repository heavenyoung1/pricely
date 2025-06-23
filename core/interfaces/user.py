from abc import ABC, abstractmethod
from typing import Optional, List

from core.models.user import User

class IUserRepo(ABC):
    @abstractmethod
    async def save(self, user: 'User') -> None:
        pass

    @abstractmethod
    async def find_by_tg_id(self, telegram_id: str) -> Optional['User']:
        pass
    
    @abstractmethod
    async def find_by_product_id(self, product_id: str) -> List['User']:
        pass