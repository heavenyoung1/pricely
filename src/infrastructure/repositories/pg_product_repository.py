from src.domain.entities.product import Product
from src.interfaces.repositories.product_repository import ProductRepository
from src.domain.entities.price import PriceStamp
from src.domain.entities.product import Product
from src.infrastructure.database.models.product import DBProduct
from src.infrastructure.database.core.database import engine, SessionFactory


from sqlalchemy.orm import Session
from typing import Optional, List, TYPE_CHECKING

# if TYPE_CHECKING:
#     from src.domain.entities.product import Product

class PGSQLProductRepository(ProductRepository):
    def __init__(self, session: Session):
        self.session = session

    def save_one_product(self, product: Product, price_stamp: PriceStamp) -> None:
        db_product = product.to_orm()
        db_price_stamp = price_stamp.to_orm()
        self.session.merge(db_product)
        self.session.add(db_price_stamp)
        self.session.commit()
            
    def save_few_products(self, products: List, price_stamp: PriceStamp) -> None:
        db_products = [product.to_orm() for product in products]
        db_price_stamp=price_stamp.to_orm()
        self.session.bulk_save_objects(db_products, update_changed_only=True)
        self.session.add(db_price_stamp)
        self.session.commit()

    def find_product_by_url(self, product_url: str) -> Optional[DBProduct]:
        db_product_url = self.session.query(DBProduct).filter(DBProduct.link == product_url)
        if not db_product_url: 
            raise
        else:
            return db_product_url
        
    def find_product_by_id(self, product_id: str) -> Optional[DBProduct]:
        db_product_id = self.session.query(DBProduct).filter(DBProduct.product_id == product_id)
        if not db_product_id: 
            raise
        else:
            return db_product_id
        
    def find_few_products_by_urls(self, product_urls: List[str]) -> List[DBProduct]:
        for product_url in product_urls:
            db_products = self.session.query(DBProduct).filter(DBProduct.link.in_(product_urls)).all()
            return [Product(**db_product.__dict__) for db_product in db_products]
                                                                  
        