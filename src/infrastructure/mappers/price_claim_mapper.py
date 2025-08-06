from src.domain.entities import PriceClaim
from src.infrastructure.database.models import ORMPriceClaim
from .price_mapper import PriceMapper



class PriceClaimMapper:
    @staticmethod
    def to_orm(price_claim: PriceClaim) -> ORMPriceClaim:
        '''Преобразовать PriceClaim в ORMPriceClaim'''
        return ORMPriceClaim(
        claim_id=price_claim.claim_id,
        product_id=price_claim.product_id,
        time_claim=price_claim.time_claim,
        price=PriceMapper.to_orm(price_claim.price, price_claim.claim_id),
        )