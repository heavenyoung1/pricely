from abc import ABC, abstractmethod
from typing import Optional, List
from src.domain.entities import User
from sqlalchemy.orm import Session

class UserRepository(ABC):
    @abstractmethod
    def save(self, user: User) -> None:
        pass

    @abstractmethod
    def get(self, user_id: str) -> Optional[User]:
        pass

    @abstractmethod
    def delete(self, user_id: str) -> None:
        pass