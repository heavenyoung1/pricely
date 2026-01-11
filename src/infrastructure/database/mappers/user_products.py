from src.domain.enttities.user_products import UserProducts
from src.infrastructure.database.models.user_products import ORMUserProducts


class UserProductsMapper:
    @staticmethod
    def to_orm(domain: UserProducts) -> 'ORMUserProducts':
        return ORMUserProducts(
            user_id=str(domain.user_id),
            product_id=str(domain.product_id),
        )

    @staticmethod
    def to_domain(orm: ORMUserProducts) -> 'UserProducts':
        return UserProducts(
            user_id=int(orm.user_id),
            product_id=int(orm.product_id),
        )
