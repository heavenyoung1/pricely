from src.domain.repositories import ProductRepository, PriceRepository, UserRepository
from src.infrastructure.repositories import ProductRepositoryImpl, PriceRepositoryImpl, UserRepositoryImpl
from src.infrastructure.database.core.database import get_db_session

class UnitOfWork:
    def __init__(self):
        self.session_factory = get_db_session()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass  # Нет общей сессии, так как @with_session в репозиториях

    def product_repository(self) -> ProductRepository:
        return ProductRepositoryImpl()

    def price_repository(self) -> PriceRepository:
        return PriceRepositoryImpl()

    def user_repository(self) -> UserRepository:
        return UserRepositoryImpl()