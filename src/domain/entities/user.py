from pydantic import BaseModel, ConfigDict

config = ConfigDict(strict=True, from_attributes=True, )


class User(BaseModel):
    id: str
    username: str
    chat_id: str
    products: str # JSON-строка с ID продуктов

    model_config = ConfigDict(
    strict=True,
    from_attributes=True
    )
