import logging

from src.application.interfaces.repositories import UserRepository
from src.infrastructure.database.mappers import UserMapper
from src.infrastructure.database.models import ORMUser

from sqlalchemy.orm import Session


logger = logging.getLogger(__name__)

class ProductUserRepositoryImpl(UserRepository):
    '''Реализация репозитория для работы с пользователями в базе данных.'''
    def __init__(self, session: Session):
        self.session = session