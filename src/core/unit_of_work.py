from typing import Callable, Type, Optional
from sqlalchemy.orm import Session

from src.application.interfaces.repositories import ProductRepository, PriceRepository, UserRepository


class UnitOfWork:
    '''
    Unit of Work для управления репозиториями и транзакциями.

    Предоставляет:
    - Централизованный доступ ко всем репозиториям
    - Управление жизненным циклом сессий (через with_session в репозиториях)
    - Единую точку для потенциального управления транзакциями
    '''

class UnitOfWork:
    def __init__(self, session_factory: Callable[[], Session]):
        self.session_factory = session_factory
        self._repositories: dict[Type, object] = {}
        self.session: Optional[Session] = None

    def __enter__(self):
        self.session = self.session_factory()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.session.rollback()
        self.session.close()
        self.session = None

    def commit(self):
        if self.session:
            self.session.commit()

    def get_repository(self, repo_type: Type):
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
                raise ValueError(f'Неизвестный тип репозитория: {repo_type}')
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