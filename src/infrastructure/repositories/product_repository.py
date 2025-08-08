from src.domain.repositories import ProductRepository
from src.domain.entities import Product
from src.infrastructure.mappers.product_mapper import ProductMapper
from src.infrastructure.database.models import ORMProduct
from src.infrastructure.database.core.database import with_session
from sqlalchemy.orm import Session

class SqlAlchemyProductRepository(ProductRepository):
    def __init__(self, session: Session):
        self.session = Session

    @with_session
    def save(product: Product, session: Session) -> None:
        orm_product = ProductMapper.to_orm(product)
        self.session.merge(orm_product)

    @with_session
    def get_
