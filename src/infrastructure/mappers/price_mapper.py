from src.domain.entities import Price
from src.interfaces.dto import PriceDTO
from src.infrastructure.database.models import PriceORM


class PriceMapper:
    @staticmethod
    def dto_to_domain(dto: PriceDTO) -> Price:
        return Price(
            id=dto.id,
            product_id=dto.product_id,
            with_card=dto.with_card,
            without_card=dto.without_card,
            previous_with_card=dto.previous_with_card,
            previous_without_card=dto.previous_without_card,
            default=dto.default,
            claim=dto.claim
        )

    @staticmethod
    def domain_to_dto(domain: Price) -> PriceDTO:
        return PriceDTO(
            id=domain.id,
            product_id=domain.product_id,
            with_card=domain.with_card,
            without_card=domain.without_card,
            previous_with_card=domain.previous_with_card,
            previous_without_card=domain.previous_without_card,
            default=domain.default,
            claim=domain.claim
        )

    @staticmethod
    def domain_to_orm(domain: Price) -> PriceORM:
        return PriceORM(
            id=domain.id,
            product_id=domain.product_id,
            with_card=domain.with_card,
            without_card=domain.without_card,
            previous_with_card=domain.previous_with_card,
            previous_without_card=domain.previous_without_card,
            default=domain.default,
            claim=domain.claim
        )

    @staticmethod
    def orm_to_domain(orm: PriceORM) -> Price:
        return Price(
            id=orm.id,
            product_id=orm.product_id,
            with_card=orm.with_card,
            without_card=orm.without_card,
            previous_with_card=orm.previous_with_card,
            previous_without_card=orm.previous_without_card,
            default=orm.default,
            claim=orm.claim
        )