from abc import ABC, abstractmethod
from typing import List


class UserProductsRepository(ABC):
    """
    Абстрактный репозиторий для работы с товарами пользователей.

    Этот интерфейс определяет методы для работы с товарами, связанными с пользователями.
    """

    @abstractmethod
    def get_products_for_user(self, user_id: str) -> List[str]:
        """
        Получить список продуктов для пользователя.

        :param user_id: Идентификатор пользователя.
        :return: Список идентификаторов продуктов, связанных с пользователем.
        """
        pass

    @abstractmethod
    def add_product_for_user(self, user_id: str, product_id: str) -> None:
        """
        Добавить товар пользователю.

        :param user_id: Идентификатор пользователя.
        :param product_id: Идентификатор продукта.
        :return: None
        """
        pass

    @abstractmethod
    def get_all_user_products_pair(self) -> List[dict]:
        """
        Получить все пары товаров и пользователей.

        Возвращает список словарей вида {'product_id': <ID продукта>, 'user_id': <ID пользователя>}.

        :return: Список всех пар товара и пользователя.
        """
        pass

    @abstractmethod
    def get_sorted_user_products(self) -> dict:
        """
        Извлекает все товары и пользователей, группируя товары по user_id.

        Возвращает словарь вида {user_id: [product_id, product_id, ...], ...}.

        :return: Словарь, где ключ - user_id, а значение - список product_id.
        """
        pass
