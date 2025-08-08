from abc import ABC, abstractmethod
from typing import Optional, List
from src.domain.entities import User
from sqlalchemy.orm import Session

class UserRepository(ABC):
    @abstractmethod
    def save(self, user: User) -> None:
        '''Сохранить или обновить пользователя.'''
        pass

    @abstractmethod
    def get(self, user_id: str) -> User:
        '''Получить пользователя по ID.'''
        pass