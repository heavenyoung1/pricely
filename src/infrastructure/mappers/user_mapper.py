from typing import TYPE_CHECKING
from src.infrastructure.database.models import ORMUser
from .product_mapper import ProductMapper

if TYPE_CHECKING:
    from src.domain.entities import User

class UserMapper:
    @staticmethod
    def to_orm(user: User) -> ORMUser:
        '''Преобразовать User в ORMUser'''
        return ORMUser(
            user_id=user.user_id,
            username=user.username,
            chat_id=user.chat_id,
            products=[
                ProductMapper.to_orm(product) for product in user.products
            ]
        )