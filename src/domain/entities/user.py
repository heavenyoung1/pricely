from pydantic import BaseModel, ConfigDict, field_validator
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .price import Price

config = ConfigDict(strict=True, from_attributes=True, )


class User(BaseModel):
    user_id: str
    username: str
    chat_id: str
    products: str # Определиться!

    model_config = ConfigDict(
    strict=True,
    from_attributes=True
    )
