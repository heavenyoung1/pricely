from src.domain.entities.product import Product
from src.interfaces.repositories.product_repository import ProductRepository
from src.domain.entities.price import PriceStamp
from src.domain.entities.product import Product
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
        self.session.merge(db_product)
        self.session.commit()
            
    def save_few_products(self, products: List, price_stamp: PriceStamp) -> None:
        # for product in products:
        #     product.to_orm()
        #     self.session.merge(product)
        db_products = [product.to_orm() for product in products]
        self.session.bulk_save_objects(db_products, update_changed_only=True)

        self.session.commit()

    def find_product_by_url(self, product_url: str) -> Optional[Product]:
        db_product_url = self.session.query(Product).filter(Product.link == product_url)
        if not db_product_url: 
            raise
        else:
            return db_product_url
        
    def find_product_by_id(self, product_id: str) -> Optional[Product]:
        db_product_id = self.session.query(Product).filter(Product.product_id == product_id)
        if not db_product_id: 
            raise
        else:
            return db_product_id
        
    def find_few_products_by_urls(self, product_urls: List) -> List[Product]:
        for product_url in product_urls:
            db_product_url = self.session.query(Product).filter(Product.link == product_url)
            if not db_product_url: 
                raise
            else:
                return db_product_url
        