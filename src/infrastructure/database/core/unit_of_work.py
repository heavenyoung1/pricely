from typing import Callable, Type
from sqlalchemy.orm import Session

from src.domain.repositories import ProductRepository, PriceRepository, UserRepository


class UnitOfWork:
    """
    Unit of Work для управления репозиториями и транзакциями.

    Предоставляет:
    - Централизованный доступ ко всем репозиториям
    - Управление жизненным циклом сессий (через with_session в репозиториях)
    - Единую точку для потенциального управления транзакциями
    """

    def __init__(self, session_factory: Callable[[], Session]):
        """
        Инициализирует Unit of Work.

        Args:
            session_factory: фабрика сессий SQLAlchemy
        """
        self.session_factory = session_factory
        self._repositories = {}
        self.session: Session | None = None

    def __enter__(self):
        """Вход в контекстный менеджер."""
        self.session = self.session_factory()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Выход из контекстного менеджера."""
        if exc_type is None:
            self.session.commit()
        else:
            self.session.rollback()
        self.session.close()
        self.session = None

    def commit(self):
        """Явно фиксирует транзакцию."""
        if self.session:
            self.session.commit()

    def get_repository(self, repo_type: Type):
        """
        Возвращает экземпляр репозитория указанного типа (ленивая инициализация).
        """
        if repo_type not in self._repositories:
            if repo_type.__name__ == 'ProductRepository':
                from src.infrastructure.repositories.product_repository import ProductRepositoryImpl
                self._repositories[repo_type] = ProductRepositoryImpl(self.session)
            elif repo_type.__name__ == 'PriceRepository':
                from src.infrastructure.repositories.price_repository import PriceRepositoryImpl
                self._repositories[repo_type] = PriceRepositoryImpl(self.session)
            elif repo_type.__name__ == 'UserRepository':
                from src.infrastructure.repositories.user_repository import UserRepositoryImpl
                self._repositories[repo_type] = UserRepositoryImpl(self.session)
            else:
                raise ValueError(f"Неизвестный тип репозитория: {repo_type}")
        return self._repositories[repo_type]

    def product_repository(self) -> ProductRepository:
        from src.infrastructure.repositories.product_repository import ProductRepositoryImpl
        return ProductRepositoryImpl(session=self.session)

    def price_repository(self) -> PriceRepository:
        from src.infrastructure.repositories.price_repository import PriceRepositoryImpl
        return PriceRepositoryImpl(session=self.session)

    def user_repository(self) -> UserRepository:
        from src.infrastructure.repositories.user_repository import UserRepositoryImpl
        return UserRepositoryImpl(session=self.session)