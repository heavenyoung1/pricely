from src.domain.enttities.user_products import UserProducts
from src.infrastructure.database.models.user_products import ORMUserProducts


class UserProductsMapper:
    @staticmethod
    def to_orm(domain: UserProducts) -> 'ORMUserProducts':
        return ORMUserProducts(
            user_id=domain.user_id,
            product_id=domain.product_id,
        )

    @staticmethod
    def to_domain(orm: ORMUserProducts) -> 'UserProducts':
        return UserProducts(
            user_id=orm.user_id,
            product_id=orm.product_id,
        )
