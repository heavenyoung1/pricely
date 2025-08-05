from typing import TYPE_CHECKING

from src.infrastructure.database.models import ORMPrice

if TYPE_CHECKING:
    from src.domain.entities import Price

class PriceMapper:
    @staticmethod
    def to_orm(price: Price, claim_id: str) -> ORMPrice:
        '''Преобразовать Price в ORMPrice'''
        return ORMPrice(
            id=claim_id, # Используем claim_id как уникальный идентификатор
            with_card=price.with_card,
            without_card=price.without_card,
            previous_with_card=price.previous_with_card,
            previous_without_card=price.previous_without_card,
            default=price.default,
            price_claims_id=claim_id,
        )