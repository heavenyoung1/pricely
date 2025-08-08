from src.domain.entities import Price
from src.infrastructure.database.models import ORMPrice

class PriceMapper:
    @staticmethod
    def to_orm(entity: Price) -> ORMPrice:
        return ORMPrice(
            id=entity.id,
            product_id=entity.product_id,
            with_card=entity.with_card,
            without_card=entity.without_card,
            previous_with_card=entity.previous_with_card,
            previous_without_card=entity.previous_without_card,
            default=entity.default,
            date_claim=entity.claim,
        )
    
    @staticmethod
    def to_domain(model: ORMPrice) -> Price:
        return Price(
            id=model.id,
            product_id=model.product_id,
            with_card=model.with_card,
            without_card=model.without_card,
            previous_with_card=model.previous_with_card,
            previous_without_card=model.previous_without_card,
            default=model.default,
            claim=model.date_claim,
        )