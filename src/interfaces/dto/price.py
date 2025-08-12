from pydantic import BaseModel
from datetime import datetime

from src.domain.entities import Price


class PriceCreateDTO(BaseModel):
    id: str
    product_id: str
    with_card: int
    without_card: int
    previous_with_card: int
    previous_without_card: int
    default: int
    claim: datetime

    def to_domain(self) -> Price:
        return Price(
            id=self.id,
            product_id=self.product_id,
            with_card=self.with_card,
            without_card=self.without_card,
            previous_with_card=self.previous_with_card,
            previous_without_card=self.previous_without_card,
            default=self.default,
            claim=self.claim
        )