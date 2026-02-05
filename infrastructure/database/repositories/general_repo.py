from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select

from infrastructure.database.models.price import ORMPrice
from infrastructure.database.models.product import ORMProduct
from infrastructure.database.models.user import ORMUser
from infrastructure.database.models.user_products import ORMUserProducts
from infrastructure.database.mappers.product import ProductMapper
from infrastructure.database.mappers.price import PriceMapper
from infrastructure.database.mappers.user import UserMapper

from domain.exceptions import DatabaseError
from core.logger import logger



class GeneralRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_records_by_changed_prices(
        self,
        price_ids: list[int],
    ) -> list[tuple]:
        try:
            if not price_ids:
                return []

            statement = (
                select(
                    ORMProduct.article,
                    ORMProduct.id.label('product_id'),
                    ORMProduct.name,
                    ORMPrice.id.label('price_id'),
                    ORMPrice.with_card.label('product_with_card'),
                    ORMPrice.without_card.label('product_without_card'),
                    ORMPrice.previous_with_card.label('product_previous_with_card'),
                    ORMPrice.previous_without_card.label('product_previous_without_card'),
                    ORMUser.name.label('username'),
                    ORMUser.id.label('user_id'),
                    ORMUser.chat_id,
                )
                .join(ORMProduct, ORMProduct.id == ORMPrice.product_id)
                .join(ORMUserProducts, ORMUserProducts.product_id == ORMProduct.id)
                .join(ORMUser, ORMUser.id == ORMUserProducts.user_id)
                .where(ORMPrice.id.in_(price_ids))
            )
            result = await self.session.execute(statement)
            rows = result.mappings().all()
            logger.debug(f'[DATA_RECORDS] {rows}')
            return rows

        except SQLAlchemyError as error:
            message = f'Ошибка при получении данных: {error}'
            logger.error(message)
            raise DatabaseError(message)