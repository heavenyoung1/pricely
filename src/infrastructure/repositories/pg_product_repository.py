from sqlalchemy.orm import Session
from src.interfaces.repositories import ProductRepository
from src.domain.entities import Product, PriceClaim
from sqlalchemy import select

from src.infrastructure.database.models import ORMroduct

class PGSQLProductRepository(ProductRepository):
    def __init__(self, session: Session):
        self.session = session

    def save_product(self, product: Product, price_claim: PriceClaim) -> None:
        '''Сохранить продукт и связанный ценовой клейм в базе данных'''
        try:
            # Создаем запрос
            stmt = select(ORMroduct).where(ORMroduct.product_id == product.product_id)

            with Session(self.engine) as session:  # self.engine - ваш движок SQLAlchemy
                result = session.execute(stmt)

        except:
            pass
                                                                  
        