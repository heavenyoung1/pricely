from domain.entities.product import Product
from infrastructure.database.models.product import ORMProduct


class ProductMapper:
    @staticmethod
    def to_orm(domain: Product) -> 'ORMProduct':
        return ORMProduct(
            id=domain.id,
            article=domain.article,
            name=domain.name,
            link=domain.link,
            change=domain.change,
        )

    @staticmethod
    def to_domain(orm: ORMProduct) -> 'Product':
        return Product(
            id=orm.id,
            article=orm.article,
            name=orm.name,
            link=orm.link,
            change=orm.change,
        )
