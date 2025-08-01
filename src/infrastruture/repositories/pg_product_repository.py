from src.domain.entities.product import Product
from src.interfaces.repositories.product_repository import ProductRepository
from src.domain.entities.price import PriceStamp

from sqlalchemy.orm import Session
from infrastruture.database.core.database import engine, SessionFactory

class PGSQLProductRepository(ProductRepository):
    def __init__(self, session: Session):
        self.session = session

    def save_one_product(self, product: Product, price_stamp: PriceStamp) -> None:
        db_product = product.to_orm()
        self.session.merge()
        self.session.commit()
            
