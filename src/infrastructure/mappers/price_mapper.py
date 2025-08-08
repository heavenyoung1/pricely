from sqlalchemy.orm import Session
from typing import TYPE_CHECKING

from src.domain.entities import Price
from src.infrastructure.database.models import ORMPrice


class PriceMapper:
    @staticmethod
    def to_orm(price: Price, session: Session) -> ORMPrice:
        '''Преобразовать Price в ORMPrice'''
        return ORMPrice(
            id=price.id,
            product_id=price.product_id,
            with_card=price.with_card,
            without_card=price.without_card,
            previous_with_card=price.previous_with_card,
            previous_without_card=price.previous_without_card,
            default=price.default,
            date_claim=price.claim,
        )