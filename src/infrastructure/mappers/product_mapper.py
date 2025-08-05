import json
from src.domain.entities import Product
from src.infrastructure.database.models import ORMProduct
from .price_claim_mapper import PriceClaimMapper

class ProductMapper:
    @staticmethod
    def to_orm(product: Product) -> ORMProduct:
        '''Преобразовать Product в ORMProduct'''
        return ORMProduct(
            product_id=product.product_id,
            user_id=product.user_id,
            name=product.name,
            link=str(product.link),
            image_url=str(product.image_url),
            rating=product.rating,
            categories=json.dumps(product.categories),
            price_claim=[
                PriceClaimMapper.to_orm(claim) for claim in product.price_claims
            ]
        )