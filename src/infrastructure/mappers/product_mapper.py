import json
from sqlalchemy.orm import Session

from src.domain.entities import Product
from src.infrastructure.database.models import ORMProduct

class ProductMapper:
    @staticmethod
    def to_orm(product: Product, session: Session = None) -> ORMProduct:
        '''Преобразовать Product в ORMProduct'''
        try:
            categories_json = json.dumps(product.categories)
        except TypeError as e:
            raise ValueError(f'ERROR - Ошибка сериалиции КАТЕГОРИИ в JSON!')


        return ORMProduct(
            id=product.product_id,
            user_id=product.user_id,
            price_id=product.price_id,
            name=product.name,
            link=str(product.link),
            image_url=str(product.image_url),
            rating=product.rating,
            categories=json.dumps(product.categories),
        )
    
    @staticmethod
    def update_orm(orm_product: ORMProduct, product: Product) -> None:
        '''Обновляет существующий ORMProduct на основе доменного Product.'''
        orm_product.user_id = product.user_id
        orm_product.name = product.name
        orm_product.link = str(product.link)
        orm_product.image_url = str(product.image_url)
        orm_product.rating = product.rating
        orm_product.categories = json.dumps(product.categories)