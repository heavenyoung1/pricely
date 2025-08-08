from src.domain.repositories import PriceRepository
from src.domain.entities import Price
from src.infrastructure.mappers.price_mapper import PriceMapper
from src.infrastructure.database.models import ORMPrice
from src.infrastructure.database.core.database import with_session
from sqlalchemy.orm import Session
from typing import List


class SqlAlchemyPriceRepository(PriceRepository):

    @with_session
    def save(self, price: Price, session: Session) -> None:
        orm_price = PriceMapper.to_orm(price)
        session.merge(orm_price)

    @with_session
    def get(self, price_id, session: Session) -> Price:
        orm_price = session.get(ORMPrice, price_id)
        return PriceMapper.to_entity(orm_price) if orm_price else None
    
    @with_session
    def get_prices_by_product(self, product_id, session: Session) -> List['Price']:
        prices = session.query(ORMPrice).filter_by(product_id=product_id).all()
        return [PriceMapper.to_entity(price) for price in prices]
        