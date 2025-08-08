from src.domain.repositories import UserRepository
from src.domain.entities import Price
from src.infrastructure.mappers.user_mapper import UserMapper
from src.infrastructure.database.models import ORMUser
from src.infrastructure.database.core.database import with_session
from sqlalchemy.orm import Session
from typing import List

class SqlAlchemyUserRepository(UserRepository):

    @with_session
    def save(self, user: User, session: Session) -> None:
        orm_user = UserMapper.to_orm(user)
        session.merge(orm_user)

    @with_session
    def get(self, user_id: str, session: Session) -> User:
        orm_user = session.get(ORMUser, user_id)
        return UserMapper.to_domain(orm_user) if orm_user else None