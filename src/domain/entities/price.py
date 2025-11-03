from dataclasses import dataclass
from datetime import datetime


@dataclass
class Price:
    """
    Доменная сущность, представляющая цену товара.

    Attributes:
        id (int): Автоинкрементный ID.
        product_id (str): Идентификатор связанного продукта.
        with_card (int): Цена с картой.
        without_card (int): Цена без карты.
        previous_with_card (int | None): Предыдущая цена с картой.
        previous_without_card (int | None): Предыдущая цена без карты.
        created_at (datetime): Дата и время клейма цены.
    """

    id: int
    product_id: str
    with_card: int
    without_card: int
    previous_with_card: int | None
    previous_without_card: int | None
    created_at: datetime
