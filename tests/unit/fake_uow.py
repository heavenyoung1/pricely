from tests.unit.fakes import InMemoryProductRepository, InMemoryPriceRepository, InMemoryUserRepository

class FakeUnitOfWork:
    def __init__(self):
        self._product_repo = InMemoryProductRepository()
        self._price_repo = InMemoryPriceRepository()
        self._user_repo = InMemoryUserRepository()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def commit(self):
        pass

    def product_repository(self):
        return self._product_repo

    def price_repository(self):
        return self._price_repo

    def user_repository(self):
        return self._user_repo