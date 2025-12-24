from src.domain.entities import Price
from src.infrastructure.database.models import ORMPrice
from deprecated import deprecated


class PriceMapper:
    @staticmethod
    def to_orm(domain: Price) -> ORMPrice:
        return ORMPrice(
            id = None,
            product_id=domain.product_id,
            with_card=domain.with_card,
            without_card=domain.without_card,
            previous_with_card=domain.previous_with_card,
            previous_without_card=domain.previous_without_card,
            created_at=domain.created_at,
        )

    @staticmethod
    def to_domain(orm: ORMPrice) -> Price:
        return Price(
            id=orm.id,
            product_id=orm.product_id,
            with_card=orm.with_card,
            without_card=orm.without_card,
            previous_with_card=orm.previous_with_card,
            previous_without_card=orm.previous_without_card,
            created_at=orm.created_at,
        )
