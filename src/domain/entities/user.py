from dataclasses import dataclass, field
from typing import List

@dataclass
class User:
    '''
    Доменная сущность, представляющая пользователя.

    Атрибуты:
        id (str): Уникальный идентификатор пользователя.
        username (str): Имя пользователя.
        chat_id (str): Идентификатор чата пользователя (вероятно нужно будет удалить, так как он равен ID)
        products (List[str]): Список идентификаторов продуктов, привязанных к пользователю.
    '''
    id: str
    username: str
    chat_id: str
    products: List[str] = field(default_factory=list)