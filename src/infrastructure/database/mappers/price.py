from src.domain.enttities.price import Price
from src.infrastructure.database.models.price import ORMPrice


class PriceMapper:
    @staticmethod
    def to_orm(domain: Price) -> 'ORMPrice':
        return ORMPrice(
            id=domain.id if domain.id else None,
            product_id=str(domain.product_id),
            with_card=domain.with_card,
            without_card=domain.without_card,
            previous_with_card=domain.previous_with_card,
            previous_without_card=domain.previous_without_card,
        )

    @staticmethod
    def to_domain(orm: ORMPrice) -> 'Price':
        return Price(
            id=orm.id,
            product_id=int(orm.product_id),
            with_card=orm.with_card,
            without_card=orm.without_card,
            previous_with_card=orm.previous_with_card if orm.previous_with_card is not None else 0,
            previous_without_card=orm.previous_without_card if orm.previous_without_card is not None else 0,
        )
