from src.application.services import ProductService
from src.domain.entities import Product, Price, User
from src.infrastructure.database.models import ORMUser, ORMProduct, ORMUser

# def test_create_user_mock(mock_product_service, mock_uow, mock_user_repo, user):
#     '''Тест успешного создания пользователя с моками (юнит-тест).'''
#     # Настраиваем моки: пользователь не существует
#     mock_user_repo.get.return_value = None

#     # Выполняем создание пользователя
#     mock_product_service.create_user(user)

#     # Проверяем, что взяли репозиторий из uow и вызвали save(get)
#     mock_uow.user_repository.assert_called_once_with()
#     mock_user_repo.get.assert_called_once_with(user.id)
#     mock_user_repo.save.assert_called_once_with(user)

def test_with_uow_commit(mock_product_service, mock_uow, user):
    """Тест декоратора with_uow с commit=True."""
    # Настраиваем моки
    mock_uow.user_repository.return_value.get.return_value = None
    mock_uow.__enter__.return_value = mock_uow
    mock_uow.__exit__.return_value = None

    # Выполняем метод с декоратором commit=True
    mock_product_service.create_user(user)

    # Проверяем, что uow_factory вызван
    mock_product_service.uow_factory.assert_called_once()
    # Проверяем, что UnitOfWork используется как контекстный менеджер
    mock_uow.__enter__.assert_called_once()
    mock_uow.__exit__.assert_called_once()
    # Проверяем, что commit вызван
    mock_uow.commit.assert_called_once()

def test_with_uow_no_commit(mock_product_service, mock_uow, product):
    """Тест декоратора with_uow с commit=False."""
    # Настраиваем моки
    mock_uow.product_repository.return_value.get.return_value = product
    mock_uow.__enter__.return_value = mock_uow
    mock_uow.__exit__.return_value = None

    # Выполняем метод с декоратором commit=False
    mock_product_service.get_product(product.id)

    # Проверяем, что uow_factory вызван
    mock_product_service.uow_factory.assert_called_once()
    # Проверяем, что UnitOfWork используется как контекстный менеджер
    mock_uow.__enter__.assert_called_once()
    mock_uow.__exit__.assert_called_once()
    # Проверяем, что commit НЕ вызван
    assert not mock_uow.commit.called, "commit не должен быть вызван"