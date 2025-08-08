import json
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.infrastructure.database.models import ORMUser, ORMProduct
from src.domain.entities import User


class UserMapper:
    @staticmethod
    def to_orm(user: User, session: Session = None) -> ORMUser:
        '''Преобразовать User в ORMUser'''
        try:
            product_ids = json.loads(user.products) if user.products else []
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to decode products JSON: {e}")

        # Создаём ORMUser
        orm_user = ORMUser(
            id=user.id,
            username=user.username,
            chat_id=user.chat_id
        )

        # Создаём заглушки ORMProduct для каждого ID
        orm_user.products = [
            ORMProduct(id=product_id) for product_id in product_ids
        ]

        return orm_user