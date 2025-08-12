from unittest.mock import MagicMock
from src.application.services import ProductService
#from src.domain.entities import Product, Price, User

def test_create_product_with_price_call_repo(product, price, user):
    uow_factory = MagicMock()
    uow = MagicMock()
    uow_factory.return_value.__enter__.return_value = uow

    # 1. Мокаем репозитории
    product_repo = MagicMock()
    price_repo = MagicMock()
    user_repo = MagicMock()
    uow.product_repository.return_value = product_repo
    uow.price_repository.return_value = price_repo
    uow.user_repository.return_value = user_repo

    # 2. Создаём сервис с моком фабрики
    service = ProductService(uow_factory)

    # Вызываем метод
    service.create_product_with_price(product, price, user)

    # Проверяем, что uow_factory вызван
    uow_factory.assert_called_once()

    # Проверяем, что методы save вызваны
    assert price_repo.save.called
    assert product_repo.save.called
    assert user_repo.save.called

    # Проверяем, что uow.commit вызван
    assert uow.commit.called