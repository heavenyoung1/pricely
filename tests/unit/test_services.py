from src.application.services import ProductService
from src.domain.entities import Product, Price, User
from src.infrastructure.database.models import ORMUser, ORMProduct, ORMUser

def test_create_user_mock(mock_product_service, mock_uow, mock_user_repo, user):
    '''ЮНИТ ТЕСТ - Провкра логики вызова, НЕ реально сохранение в БД. '''
    # Настраиваем моки: пользователь не существует
    mock_product_service.create_user(user)

    # uow_factory вызван
    mock_product_service.uow_factory.assert_called_once()
    created_uow = mock_product_service.uow_factory.return_value

    # user_repository вызван
    created_uow.user_repository.assert_called_once_with()

    # save вызван, get — нет (т.к. use_case просто сохраняет пользователя)
    created_repo = created_uow.user_repository.return_value
    created_repo.save.assert_called_once_with(user)
    created_repo.get.assert_not_called()

def test_create_product_mock(mock_product_service, mock_uow, mock_product_repo, product):
    '''ЮНИТ ТЕСТ - Провкра логики вызова, НЕ реально сохранение в БД. '''
    # 1. Arrange (подготовка), 
    # Какая подготовка должна быть? Создание продукта для проверки вызова репозиториев?
    mock_product_service.create_product(product)
    created_uow = mock_product_service.uow_factory.return_value

    created_uow.product_repository.return_value
    
    created_repo = created_uow.product_repository.return_value
    created_repo.save.assert_called_once_with(product)
    created_repo.get.assert_not_called()

    



# def test_create_user_mock(mock_product_service, mock_uow, mock_user_repo, user):
#     '''ЮНИТ ТЕСТ - Провкра логики вызова, НЕ реально сохранение в БД. '''
#     # Настраиваем моки: пользователь не существует
#     mock_product_service.create_user(user)

#     # uow_factory вызван
#     mock_product_service.uow_factory.assert_called_once()
#     created_uow = mock_product_service.uow_factory.return_value

#     # user_repository вызван
#     created_uow.user_repository.assert_called_once_with()

#     # save вызван, get — нет (т.к. use_case просто сохраняет пользователя)
#     created_repo = created_uow.user_repository.return_value
#     created_repo.save.assert_called_once_with(user)
#     created_repo.get.assert_not_called()