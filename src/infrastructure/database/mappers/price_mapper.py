from src.domain.entities import Price
from src.application.dto import PriceDTO
from src.infrastructure.database.models import ORMPrice


class PriceMapper:
    @staticmethod
    def dto_to_domain(dto: PriceDTO) -> Price:
        return Price(
            id=int(dto.id),  # Преобразуем str в int
            product_id=dto.product_id,
            with_card=dto.with_card,
            without_card=dto.without_card,
            previous_with_card=dto.previous_with_card,
            previous_without_card=dto.previous_without_card,
            default=dto.default,
            created_at=dto.created_at,
        )
    
    @staticmethod
    def domain_to_dto(domain: Price) -> PriceDTO:
        return PriceDTO(
            id=str(domain.id),  # Преобразуем int в str
            product_id=domain.product_id,
            with_card=domain.with_card,
            without_card=domain.without_card,
            previous_with_card=domain.previous_with_card,
            previous_without_card=domain.previous_without_card,
            default=domain.default,
            created_at=domain.created_at,
        )

    @staticmethod
    def domain_to_orm(domain: Price) -> ORMPrice:
        return ORMPrice(
            id=domain.id,
            product_id=domain.product_id,
            with_card=domain.with_card,
            without_card=domain.without_card,
            previous_with_card=domain.previous_with_card,
            previous_without_card=domain.previous_without_card,
            default=domain.default,
            created_at=domain.created_at,
        )

    @staticmethod
    def orm_to_domain(orm: ORMPrice) -> Price:
        return Price(
            id=orm.id,
            product_id=orm.product_id,
            with_card=orm.with_card,
            without_card=orm.without_card,
            previous_with_card=orm.previous_with_card,
            previous_without_card=orm.previous_without_card,
            default=orm.default,
            created_at=orm.created_at,
        )