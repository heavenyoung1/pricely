from src.domain.enttities.product import Product
from src.infrastructure.database.models.product import ORMProduct


class ProductMapper:
    def to_orm(domain: Product) -> "ORMProduct":
        return ORMProduct(
            id=domain.id,
            name=domain.name,
            link=domain.link,
        )

    def to_domain(orm: ORMProduct) -> "Product":
        return Product(
            id=orm.id,
            name=orm.name,
            link=orm.link,
        )
