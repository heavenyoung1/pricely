from abc import ABC, abstractmethod

from core.models.price import Price

class IPriceRepo(ABC):
    @abstractmethod
    async def save(self, price: 'Price') -> None:
        pass