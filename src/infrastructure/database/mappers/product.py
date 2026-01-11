from src.domain.entities.product import Product
from src.infrastructure.database.models.product import ORMProduct


class ProductMapper:
    @staticmethod
    def to_orm(domain: Product) -> 'ORMProduct':
        return ORMProduct(
            id=domain.id,
            article=domain.articule,
            name=domain.name,
            link=domain.link,
        )

    @staticmethod
    def to_domain(orm: ORMProduct) -> 'Product':
        return Product(
            id=orm.id,
            article=orm.articule,
            name=orm.name,
            link=orm.link,
        )
