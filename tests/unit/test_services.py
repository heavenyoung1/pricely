from unittest.mock import MagicMock
from src.application.services import ProductService

def test_create_product_with_price_call_repo():
    # uow_factory = MagicMock()
    # service = ProductService(MagicMock)
    # product, price, user = MagicMock(), MagicMock(), MagicMock()

    # service.create_product_with_price(product, price, user)

    # uow = uow_factory()
    # assert uow.product_repository().save.called
    # assert uow.price_repository().save.called
    # assert uow.user_repository().save.called

    # 1. Создаём мок uow_factory и настраиваем цепочку вызовов
    mock_uow = MagicMock()
    mock_uow_factory = MagicMock(return_value=mock_uow)
    
    # 2. Создаём сервис с моком фабрики
    service = ProductService(mock_uow_factory)
    
    # 3. Создаём тестовые данные (можно использовать MagicMock или реальные объекты)
    product, price, user = MagicMock(), MagicMock(), MagicMock()
    
    # 4. Вызываем тестируемый метод
    service.create_product_with_price(product, price, user)
    
    # 5. Проверяем вызовы
    # Проверяем, что uow_factory был вызван
    mock_uow_factory.assert_called_once()
    
    # Проверяем, что репозитории были вызваны через use case
    # (адаптируйте под реальную структуру ваших use cases)
    assert mock_uow.product_repository.called
    assert mock_uow.price_repository.called
    assert mock_uow.user_repository.called
    
    # Проверяем, что commit был вызван
    mock_uow.commit.assert_called_once()
