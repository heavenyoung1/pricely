from src.domain.repositories import UserRepository
from src.domain.entities import User
from src.infrastructure.mappers.user_mapper import UserMapper
from src.infrastructure.database.models import ORMUser
from src.infrastructure.database.core.database import with_session


class SqlAlchemyUserRepository(UserRepository):
    @with_session
    def save(self, user: User, session):
        orm_user = UserMapper.to_orm(user)
        session.merge(orm_user)