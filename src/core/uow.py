from .uow_interface import UnitOfWork
from src.core.database import get_db_session
from typing import Optional
from sqlalchemy.orm import Session
import logging

logger = logging.getLogger(__name__)

class SQLAlchemyUnitOfWork(UnitOfWork):
    '''Реализация Unit of Work для SQLAlchemy.'''
    def __init__(self, session_factory=None):
        '''
        Инициализация Unit of Work.
        
        Args:
            session_factory: Фабрика для создания сессий БД. Если не передана,
                           используется стандартная get_db_session.
        '''
        # Выбираем фабрику сессий: если передали свою - используем её,
        # если нет - используем стандартную функцию get_db_session
        # Это нужно для гибкости: в тестах можем передать другую фабрику
        self._session_factory = session_factory or get_db_session
        
        # Сессия БД. Пока None - создадим позже, когда войдем в контекст (with)
        # Optional[Session] означает "может быть Session, а может быть None"
        # Изначально None потому что сессия еще не создана
        self._session: Optional[Session] = None

    def __enter__(self):
        self._session_context = self._session_factory()
        self._session = self._session_context.__enter__()

        # Инициализируем репозитории с одной сессией
        from src.infrastructure.database.repositories import (
            ProductRepositoryImpl,
            PriceRepositoryImpl,
            UserRepositoryImpl,
        )

        self.products = ProductRepositoryImpl(self._session)
        self.prices = PriceRepositoryImpl(self._session)
        self.users = UserRepositoryImpl(self._session)

        logger.info('Unit Of Work инициализирован')
        return self