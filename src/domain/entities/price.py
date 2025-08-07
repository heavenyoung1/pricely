from pydantic import BaseModel, ConfigDict
from datetime import datetime

class Price(BaseModel):
    id: str
    product_id: str
    with_card: int
    without_card: int
    previous_with_card: int
    previous_without_card: int
    default: int
    claim: datetime

    model_config = ConfigDict(
    strict=True,
    from_attributes=True
    )