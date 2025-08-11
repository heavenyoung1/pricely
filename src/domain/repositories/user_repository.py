from abc import ABC, abstractmethod
from typing import Optional, List
from src.domain.entities import User
from sqlalchemy.orm import Session

class UserRepository(ABC):
    @abstractmethod
    def save(self, user: User) -> None:
        '''
        Сохраняет или обновляет пользователя в хранилище.
        
        Args:
            user (User): Объект пользователя для сохранения
            
        Raises:
            DatabaseError: Если произошла ошибка при работе с БД
            ValueError: Если данные пользователя невалидны
        '''
        pass

    @abstractmethod
    def get(self, user_id: str) -> Optional[User]:
        '''
        Получает пользователя по идентификатору.
        
        Args:
            user_id (str): Уникальный идентификатор пользователя
            
        Returns:
            Optional[User]: Найденный пользователь или None, если не существует
        '''
        pass

    @abstractmethod
    def delete(self, user_id: str) -> None:
        '''
        Удаляет пользователя из хранилища.
        
        Args:
            user_id (str): Уникальный идентификатор пользователя
            
        Raises:
            DatabaseError: Если произошла ошибка при удалении
        '''
        pass