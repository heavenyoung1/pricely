from src.domain.entities import Product
from src.interfaces.dto import ProductDTO
from src.infrastructure.database.models import ProductORM


class ProductMapper:
    @staticmethod
    def dto_to_domain(dto: ProductDTO) -> Product:
        return Product(
            id=dto.id,
            user_id=dto.user_id,
            price_id='',  # заполнит UseCase
            name=dto.name,
            link=str(dto.link),
            image_url=str(dto.image_url),
            rating=dto.rating,
            categories=dto.categories,
        )

    @staticmethod
    def domain_to_dto(domain: Product) -> ProductDTO:
        return ProductDTO(
            id=domain.id,
            user_id=domain.user_id,
            name=domain.name,
            link=domain.link,
            image_url=domain.image_url,
            rating=domain.rating,
            categories=domain.categories
        )

    @staticmethod
    def domain_to_orm(domain: Product) -> ProductORM:
        return ProductORM(
            id=domain.id,
            user_id=domain.user_id,
            price_id=domain.price_id,
            name=domain.name,
            link=domain.link,
            image_url=domain.image_url,
            rating=domain.rating,
            categories=domain.categories
        )

    @staticmethod
    def orm_to_domain(orm: ProductORM) -> Product:
        return Product(
            id=orm.id,
            user_id=orm.user_id,
            price_id=orm.price_id,
            name=orm.name,
            link=orm.link,
            image_url=orm.image_url,
            rating=orm.rating,
            categories=list(orm.categories) if orm.categories else []
        )