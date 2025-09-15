from pydantic import HttpUrl
from datetime import datetime
import json
from src.domain.entities import Product
from src.application.dto import ProductDTO
from src.infrastructure.database.models import ORMProduct


class ProductMapper:
    @staticmethod
    def dto_to_domain(dto: ProductDTO) -> Product:
        return Product(
            id=dto.id,
            user_id=dto.user_id,
            price_id='',  # Заполняется в UseCase
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
            link=HttpUrl(domain.link),
            image_url=HttpUrl(domain.image_url),
            rating=domain.rating,
            categories=domain.categories,
        )

    @staticmethod
    def domain_to_orm(domain: Product) -> ORMProduct:
        return ORMProduct(
            id=domain.id,
            name=domain.name,
            link=domain.link,
            image_url=domain.image_url,
            rating=domain.rating,
            categories=json.dumps(domain.categories),
        )

    @staticmethod
    def orm_to_domain(orm: ORMProduct) -> Product:
        return Product(
            id=orm.id,
            user_id='',  # Убрано, так как нет в ORM
            name=orm.name,
            link=orm.link,
            image_url=orm.image_url,
            rating=orm.rating,
            categories=json.loads(orm.categories) if orm.categories else [],
        )