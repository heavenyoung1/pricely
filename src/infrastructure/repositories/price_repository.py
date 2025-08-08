from src.domain.repositories import PriceRepository
from src.domain.entities import Price
from src.infrastructure.mappers.price_mapper import PriceMapper
from src.infrastructure.database.models import ORMPrice
from src.infrastructure.database.core.database import with_session


class SqlAlchemyPriceRepository(PriceRepository):

    @with_session
    def save(self, price: Price, session):
        orm_price = PriceMapper.to_orm(price)
        session.merge(orm_price)