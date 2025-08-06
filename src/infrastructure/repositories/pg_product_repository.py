from sqlalchemy.orm import Session
from src.interfaces.repositories import ProductRepository
from src.domain.entities import Product, PriceClaim
from src.infrastructure.database.core import with_session

from src.infrastructure.mappers import ProductMapper, PriceClaimMapper
from sqlalchemy import select

from src.infrastructure.database.models import ORMProduct

class PGSQLProductRepository(ProductRepository):
    @with_session
    def save_product(self, product: Product, price_claim: PriceClaim, session: Session = None) -> None:
        '''Сохранить продукт и связанный ценовой клейм в базе данных'''
        
        # Проверяем, существует ли продукт
        stmt = select(ORMProduct).where(ORMProduct.product_id == product.product_id)
        existing_product = session.execute(stmt).scalar_one_or_none()

        if existing_product:
            # Обновляем существующий продукт
            orm_product = ProductMapper.to_orm(product)
            existing_product.user_id = orm_product.user_id
            existing_product.name = orm_product.name
            existing_product.link = orm_product.link
            existing_product.image_url = orm_product.image_url
            existing_product.rating = orm_product.rating
            existing_product.categories = orm_product.categories

            # Добавляем новый ценовой клейм
            orm_price_claim = PriceClaimMapper(price_claim)
            existing_product.price_claims.append(price_claim)

        if not existing_product:
            # Создаем новый продукт с ценовым клеймом
            orm_product = ProductMapper.to_orm(product)
            orm_price_claim = PriceClaimMapper.to_orm(price_claim)
            orm_product.price_claims.append(orm_price_claim)
            session.add(orm_product)
                                                                  
        