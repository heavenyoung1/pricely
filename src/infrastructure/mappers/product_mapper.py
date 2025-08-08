import json
from src.domain.entities import Product
from src.infrastructure.database.models import ORMProduct

# Инфраструктура — ORM-модели и мапперы
# Тут остаются SQLAlchemy-модели, но мапперы теперь работают с чистыми доменными сущностями

class ProductMapper:
    @staticmethod
    def to_orm(entity: Product) -> Product:
        return ORMProduct(
            id=entity.id,
            user_id=entity.user_id,
            price_id=entity.price_id,
            name=entity.name,
            link=entity.link,
            image_url=entity.image_url,
            rating=entity.rating,
            categories=json.dumps(entity.categories),
        )
    
    def to_entity(model: ORMProduct) -> Product:
        return Product(
            id=model.id,
            user_id=model.user_id,
            price_id=model.price_id,
            name=model.name,
            link=model.link,
            image_url=model.image_url,
            rating=model.rating,
            categories=json.loads(model.categories),
        )
    
