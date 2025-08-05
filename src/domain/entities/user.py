from pydantic import BaseModel, ConfigDict, field_validator
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .price import Price

config = ConfigDict(strict=True, from_attributes=True, )


class User(BaseModel):
    user_id: str
    username: str
    chat_id: str
    products: str

    model_config = ConfigDict(
    strict=True,
    from_attributes=True
    )

    @field_validator('username')
    def validate_username(cls, value: str) -> str:
        if not value.strip():
            raise ValueError('Username не может быть пустым')
