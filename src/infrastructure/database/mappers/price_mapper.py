from src.domain.entities import Price
from src.application.dto import PriceDTO
from src.infrastructure.database.models import ORMPrice


class PriceMapper:
    @staticmethod
    def dto_to_domain(dto: PriceDTO) -> Price:
        return Price(
            id=dto.id,  # теперь может быть None
            product_id=dto.product_id,
            with_card=dto.with_card,
            without_card=dto.without_card,
            previous_with_card=dto.previous_with_card,
            previous_without_card=dto.previous_without_card,
            #default_price=dto.default_price,
            created_at=dto.created_at,
        )

    @staticmethod
    def domain_to_dto(domain: Price) -> PriceDTO:
        return PriceDTO(
            id=domain.id, # None до сохранения в БД → норм
            product_id=domain.product_id,
            with_card=domain.with_card,
            without_card=domain.without_card,
            previous_with_card=domain.previous_with_card,
            previous_without_card=domain.previous_without_card,
            #default_price=domain.default_price,
            created_at=domain.created_at,
        )

    @staticmethod
    def domain_to_orm(domain: Price) -> ORMPrice:
        return ORMPrice(
            # id не задаём руками, автоинкремент!!!
            product_id=domain.product_id,
            with_card=domain.with_card,
            without_card=domain.without_card,
            previous_with_card=domain.previous_with_card,
            previous_without_card=domain.previous_without_card,
            #default_price=domain.default_price,
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
            #default_price=orm.default_price,
            created_at=orm.created_at,
        )