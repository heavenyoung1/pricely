from src.application.services import ProductService
from src.domain.entities import Product, Price, User
from src.infrastructure.database.models import ORMUser, ORMProduct, ORMUser

def test_create_user_mock(mock_product_service, mock_uow, mock_user_repo, user):
    '''Тест успешного создания пользователя с моками (юнит-тест).'''
    # Настраиваем моки: пользователь не существует
    mock_user_repo.get.return_value = None

    # Выполняем создание пользователя
    mock_product_service.create_user(user)

    # Проверяем, что взяли репозиторий из uow и вызвали save(get)
    mock_uow.user_repository.assert_called_once_with()
    mock_user_repo.get.assert_called_once_with(user.id)
    mock_user_repo.save.assert_called_once_with(user)

