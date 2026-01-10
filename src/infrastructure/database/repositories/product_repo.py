from sqlalchemy.ext.asyncio import AsyncSession

from src.core.logger import logger
from src.domain.enttities.product import Product
from src.infrastructure.database.models.product import ORMProduct


# class ProductRepository():
#     def __init__(self, session: AsyncSession):
#         self.session = session

#     async def save(product: Product) -> 'Product':
#         try:
#             existing = await self.session.get(ORMProduct, product.id)
#             if existing:
#                 logger.warning(f'Товар {product.name} уже существует')

#         except:
