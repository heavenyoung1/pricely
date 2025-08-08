from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.domain.entities import User

class UserRepository(ABC):
    @abstractmethod
    def save_user(self, user: User) -> None:
        '''Сохранить или обновить пользователя.'''
        pass

    @abstractmethod
    def get_user(self, user_id: str) -> User:
        '''Получить пользователя по ID.'''
        pass