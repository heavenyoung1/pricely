from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from typing import List, TYPE_CHECKING

from .base import Base

if TYPE_CHECKING:
    from .product import DBProduct

class DBUser(Base):
    '''Модель пользователя для БД
    
    Attributes:
        id: Уникальный идентификатор пользователя
        name: Имя пользователя
        products: Список продуктов пользователя (отношение один-ко-многим)
    '''
    __tablename__ = 'users'

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    products: Mapped[List['DBProduct']] = relationship(
        back_populates="user", 
        cascade="all, delete-orphan"
    ) # Каскадное удаление