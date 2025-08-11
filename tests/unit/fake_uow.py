from tests.unit.fakes import InMemoryProductRepository, InMemoryPriceRepository, InMemoryUserRepository

class FakeUnitOfWork:
    def __init__(self):
        self._products = InMemoryProductRepository()
        self._prices = InMemoryPriceRepository()
        self._users = InMemoryUserRepository()
        self.committed = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # При ошибке автоматически откатываем
        if exc_type is not None:
            self.rollback()
        return False

    def commit(self):
        self.committed = True

    def rollback(self):
        self.committed = False

    def product_repository(self) -> InMemoryProductRepository:
        return self._products

    def price_repository(self) -> InMemoryPriceRepository:
        return self._prices

    def user_repository(self) -> InMemoryUserRepository:
        return self._users