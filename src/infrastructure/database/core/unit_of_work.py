from src.domain.repositories import ProductRepository, PriceRepository, UserRepository
from src.infrastructure.repositories import ProductRepositoryImpl, PriceRepositoryImpl, UserRepositoryImpl
from src.infrastructure.database.core.database import get_db_session

class UnitOfWork:
    '''
    Unit of Work для управления репозиториями и транзакциями.
    
    Предоставляет:
    - Централизованный доступ ко всем репозиториям
    - Управление жизненным циклом сессий (через with_session в репозиториях)
    - Единую точку для потенциального управления транзакциями
    
    Пример использования:
    >> with UnitOfWork() as uow:
    ..     repo = uow.product_repository()
    ..     product = repo.get(product_id)
    '''
    def __init__(self, session_factory: Callable[[], Session]):
        '''Инициализирует Unit of Work.
        
        Создает фабрику сессий для использования репозиториями.'''
        self.session_factory = session_factory
        self._repositories = {}

    def __enter__(self):
        '''Вход в контекстный менеджер.
        
        Returns:
            UnitOfWork: Текущий экземпляр UnitOfWork'''
        self.session = self.session_factory()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        '''Выход из контекстного менеджера.
        
        Args:
            exc_type: Тип исключения (если было)
            exc_val: Экземпляр исключения
            exc_tb: Traceback объекта'''
        if exc_type is None:
            self.session.commit()
        else:
            self.session.rollback()
        self.session.close()

    def commit(self):
        """Явно фиксирует транзакцию."""
        self.session.commit()

    def get_repository(self, repo_type: Type):
        if repo_type not in self._repositories:
            # Ленивая загрузка репозиториев
            if repo_type.__name__ == 'ProductRepository':
                from src.infrastructure.repositories.product_repository import ProductRepositoryImpl
                self._repositories[repo_type] = ProductRepositoryImpl(self.session)
            elif repo_type.__name__ == 'PriceRepository':
                from src.infrastructure.repositories.price_repository import PriceRepositoryImpl
                self._repositories[repo_type] = PriceRepositoryImpl(self.session)
            elif repo_type.__name__ == 'UserRepository':
                from src.infrastructure.repositories.user_repository import UserRepositoryImpl
                self._repositories[repo_type] = UserRepositoryImpl(self.session)
        return self._repositories[repo_type]

    def product_repository(self) -> ProductRepository:
        '''Создает и возвращает репозиторий продуктов.
        
        Returns:
            ProductRepository: Реализация репозитория продуктов'''
        return ProductRepositoryImpl(session=self.session)

    def price_repository(self) -> PriceRepository:
        '''Создает и возвращает репозиторий цен.
        
        Returns:
            PriceRepository: Реализация репозитория цен'''
        return PriceRepositoryImpl(session=self.session)

    def user_repository(self) -> UserRepository:
        '''Создает и возвращает репозиторий пользователей.
        
        Returns:
            UserRepository: Реализация репозитория пользователей'''
        return UserRepositoryImpl(session=self.session)