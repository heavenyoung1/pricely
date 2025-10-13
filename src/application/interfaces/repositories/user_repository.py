from abc import ABC, abstractmethod
from typing import Optional
from src.domain.entities import User

class UserRepository(ABC):
    '''
    Абстрактный репозиторий для работы с пользователями.

    Этот интерфейс определяет методы для получения, сохранения и удаления пользователей.
    '''
    
    @abstractmethod
    def save(self, user: User) -> None:
        '''
        Сохраняет или обновляет пользователя в репозитории.

        :param user: Объект типа User, который нужно сохранить или обновить.
        :return: None
        '''
        pass

    @abstractmethod
    def get(self, user_id: str) -> Optional[User]:
        '''
        Получает пользователя по идентификатору.

        :param user_id: Идентификатор пользователя.
        :return: Объект User, если найден, иначе None.
        '''
        pass

    @abstractmethod
    def delete(self, user_id: str) -> None:
        '''
        Удаляет пользователя по идентификатору.

        :param user_id: Идентификатор пользователя, которого нужно удалить.
        :return: None
        '''
        pass
