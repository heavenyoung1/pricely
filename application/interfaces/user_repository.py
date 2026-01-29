from abc import ABC, abstractmethod
from typing import Optional

from domain.entities.user import User


class IUserRepository(ABC):
    @abstractmethod
    async def save(self, user: User) -> User:
        '''Сохранить пользователя'''
        pass

    @abstractmethod
    async def get(self, id: int) -> Optional[User]:
        '''Получить пользователя по ID'''
        pass

    @abstractmethod
    async def update(self, user: User) -> User:
        '''Обновить пользователя'''
        pass

    @abstractmethod
    async def delete(self, id: int) -> bool:
        '''Удалить пользователя по ID'''
        pass
