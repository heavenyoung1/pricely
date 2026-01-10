from sqlalchemy.ext.asyncio import AsyncSession


class UnitOfWork:
    def __init__(self, session: AsyncSession):
        self.session = session

        # Инициализация репозиториев с общей сессией
        # self.user_repo = UserRepository(session)
        # self.product_repo = ProductRepository(session)
        # self.price_repo = PriceRepository(session)
        # self.user_products_repo = UserProductsRepository(session)
