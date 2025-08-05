from pydantic import BaseModel, ConfigDict

class Price(BaseModel):
    with_card: int
    without_card: int
    previous_with_card: int
    previous_without_card: int
    default: int

    model_config = ConfigDict(
    strict=True,
    from_attributes=True
    )