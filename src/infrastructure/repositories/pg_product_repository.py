from sqlalchemy.orm import Session
from src.interfaces.repositories import ProductRepository
from src.domain.entities import Product, Price
from src.infrastructure.database.core import with_session

from src.infrastructure.mappers import ProductMapper, PriceMapper
from sqlalchemy import select

from src.infrastructure.database.models import ORMProduct, ORMPrice

class PGSQLProductRepository(ProductRepository):
    @with_session
    def save_product(self, product: Product, price: Price , session: Session = None) -> None:
        '''Сохранить продукт и связанный ценовой клейм в базе данных'''
        
        # Проверяем, существует ли товар
        stmt = select(ORMProduct).where(ORMProduct.product_id == product.product_id)
        existing_product = session.execute(stmt).scalar_one_or_none()     

        # Проверяем, существует ли цена
        stmt = select(ORMPrice).where(ORMPrice.id == price.id)
        existing_price = session.execute(stmt).scalar_one_or_none()

        # Если цена уже существует, обновляем её
        if existing_price:
            existing_price.with_card = price.with_card
            existing_price.without_card = price.without_card
            existing_price.previous_with_card = price.previous_with_card
            existing_price.previous_without_card = price.previous_without_card
            existing_price.default = price.default
            existing_price.date_claim = price.claim
        else:
            # Создаём новую цену
            orm_price = PriceMapper.to_orm(price, session)
            session.add(orm_price)

        if existing_product:
            # Обновляем существующий продукт
            ProductMapper.update_orm(existing_product, product)
            existing_product.price_id = price.id
        else:
            # Создаём новый продукт
            orm_product = ProductMapper.to_orm(product, session)
            orm_product.price_id = price.id
            session.add(orm_product)


