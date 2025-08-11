from tests.unit.fakes import InMemoryProductRepository, InMemoryPriceRepository, InMemoryUserRepository

class FakeUnitOfWork:
    def __init__(self):
        self.product_repository = InMemoryProductRepository()
        self.price_repository = InMemoryPriceRepository()
        self.user_repository = InMemoryUserRepository()
        self.committed = False


    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass

    def commit(self):
        self.committed = True