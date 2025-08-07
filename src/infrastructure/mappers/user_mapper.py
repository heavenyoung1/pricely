from typing import TYPE_CHECKING
from sqlalchemy.orm import Session
from src.infrastructure.database.models import ORMUser
from .product_mapper import ProductMapper

if TYPE_CHECKING:
    from src.domain.entities import User

class UserMapper:
    @staticmethod
    def to_orm(user: User, session: Session = None, include_products: bool = False) -> ORMUser:
        '''Преобразовать User в ORMUser'''
        orm_user =  ORMUser(
            user_id=user.user_id,
            username=user.username,
            chat_id=user.chat_id,
            # products=[
            #     ProductMapper.to_orm(product) for product in user.products
            # ]
        )
        if include_products and user.products:
            orm_user.products = [ProductMapper.to_orm(product, session) for product in user.products]