import logging

from src.domain.repositories import ProductRepository, PriceRepository, UserRepository
from src.infrastructure.mappers import ProductMapper, PriceMapper, UserMapper
from src.infrastructure.database.models import ORMProduct, ORMPrice, ORMUser
from sqlalchemy.orm import Session


logger = logging.getLogger(__name__)

class UserRepositoryImpl(UserRepository):
    def __init__(self, session: Session):
        self.session = session

    def save(self, user):
        self.session.merge(UserMapper.to_orm(user))

    def get(self, user_id):
        orm_user = self.session.get(ORMUser, user_id)
        return UserMapper.to_domain(orm_user) if ORMUser else None