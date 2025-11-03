from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from . import Price


@dataclass
class Product:
    """
    Доменная сущность, представляющая продукт.

    Атрибуты:
        id (str): Артикул товара, представляющий его уникальный идентификатор.
        user_id (str): Идентификатор пользователя, связанного с продуктом.
        name (str): Название продукта.
        link (str): Ссылка на страницу продукта.
        image_url (str): URL изображения продукта.
        rating (float): Рейтинг продукта.
        categories (str): Категории, к которым относится продукт.
        prices (List[Price]): Список цен продукта.
    """

    id: str  # Артикул из 10 цифр
    user_id: str  # Связь с пользователем (заполняется в UseCase)
    name: str
    link: str
    image_url: str
    rating: float
    categories: str
    prices: List["Price"] = field(default_factory=list)

    @property
    def latest_price(self) -> Optional["Price"]:
        """
        Возвращает последнюю цену товара на основе времени создания (created_at) и ID.

        Если список цен пуст, возвращает None. Сортирует цены по created_at (убывание),
        и по id (убывание) для получения последней актуальной цены.

        :return: Последняя цена или None, если цен нет.
        """
        if not self.prices:
            return None
        # Сортируем по created_at (убывание) и id (убывание) для выбора последней цены
        return max(
            self.prices, key=lambda p: (p.created_at or datetime.min, p.id or "0")
        )
