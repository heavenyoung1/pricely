import json
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.infrastructure.database.models import ORMUser, ORMProduct
from src.domain.entities import User


class UserMapper:
    @staticmethod
    def to_orm(user: User, session: Session = None) -> ORMUser:
        '''Преобразовать User в ORMUser'''
        orm_user = ORMUser(
            user_id=user.user_id,
            username=user.username,
            chat_id=user.chat_id
        )
        # Если products — строка JSON, загружаем продукты
        if user.products and session:
            try:
                product_ids = json.loads(user.products)
                orm_user.products = session.execute(
                    select(ORMProduct).where(ORMProduct.id.in_(product_ids))
                ).scalars().all()
            except json.JSONDecodeError:
                raise ValueError('ERROR - Invalid JSON in User.products')
        return orm_user