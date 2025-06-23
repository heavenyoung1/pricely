from abc import ABC, abstractmethod

from core.models.user import User

class INotifier(ABC):
    @abstractmethod
    async def notify(self, user: 'User', message: str) -> None:
        pass