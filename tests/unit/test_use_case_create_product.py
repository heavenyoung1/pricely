import pytest
import json
from unittest.mock import patch, MagicMock
from src.application.use_cases.create_product import CreateProductUseCase
from src.domain.entities import Product, Price, User
from src.infrastructure.mappers import ProductMapper
from src.infrastructure.database.models import ORMUser
from src.infrastructure.core.ozon_parser import OzonParser

@patch('src.application.use_cases.create_product.uuid.uuid4')  # Патчим UUID в нужном модуле
def test_create_product_use_case_success(
        mock_uuid,
        mock_parser,
        mock_product_repo, 
        mock_price_repo, 
        mock_user_repo, 
        product, 
        price, 
        user,
    ):
    
    # Простая настройка мока UUID
    mock_uuid_instance = MagicMock()
    mock_uuid_instance.__str__ = MagicMock(return_value='pr1')
    mock_uuid.return_value = mock_uuid_instance

    # Настраиваем моки
    mock_user_repo.get.return_value = None      # Пользователь не существует
    mock_product_repo.get.return_value = None   # Товар не существует

    # Создаём use case
    use_case = CreateProductUseCase(
        product_repo=mock_product_repo,
        price_repo=mock_price_repo,
        user_repo=mock_user_repo,
        parser=mock_parser, #без () возвращаем словарь а не объект!
    )
    # Выполняем создание продукта
    use_case.execute(user_id=user.id, url=product.link)

    mock_parser.parse_product.assert_called_once_with(product.link)
    mock_product_repo.save.assert_called_once_with(product)
    mock_price_repo.save.assert_called_once_with(price)



# def test_create_product_use_case_product_exists(
#         mock_product_repo, 
#         mock_price_repo, 
#         mock_user_repo, 
#         product, 
#         price, 
#         user,
#         mock_parser,
# ):
#     '''Юнит-тест: ошибка, если продукт уже существует.'''
#     # Настраиваем моки
#     mock_user_repo.get.return_value = user      # Пользователь существует
#     mock_product_repo.get.return_value = product   # Товар не существует

#     # Создаём use case
#     use_case = CreateProductUseCase(
#         product_repo=mock_product_repo,
#         price_repo=mock_price_repo,
#         user_repo=mock_user_repo,
#         parser=mock_parser(),
#     )

#     # Выполняем создание товара
#     # with pytest.raises(ProductCreationError, match=f'Товар {product.id} уже существует'):
#     #     use_case.execute(product=product, user_id=user.id, price=price)

#     #mock_user_repo.get.assert_called_once_with(user.id)
#     mock_product_repo.get.assert_called_once_with(product.id)
#     assert not mock_price_repo.save.called, 'save (цена) не должен быть вызван'
#     assert not mock_product_repo.save.called, 'save (продукт) не должен быть вызван'
#     #assert not mock_user_repo.save.called, 'save (пользователь) не должен быть вызван'


# def test_create_product_use_case_user_not_found(
#         mock_product_repo, 
#         mock_price_repo, 
#         mock_user_repo, 
#         product, 
#         price, 
#         user,
#         mock_parser,
#         ):
#     '''Юнит-тест: ошибка, если пользователь не найден.'''
#     mock_user_repo.get.return_value = None      # Пользователь НЕ существует

#     # Создаём use case
#     use_case = CreateProductUseCase(
#         product_repo=mock_product_repo,
#         price_repo=mock_price_repo,
#         user_repo=mock_user_repo,
#         parser=mock_parser(),
#     )

#     # Выполняем создание товара
#     # with pytest.raises(ProductCreationError, match=f'Пользователь {user.id} не найден'):
#     #     use_case.execute(product=product, user_id=user.id, price=price)

#     mock_user_repo.get.assert_called_once_with(user.id)
#     # Вот эта строка нужна чтобы убедиться, что выполнение метода execute остановилось на нужной строке
#     # В нашем случае строка 29 -> existing_product = self.product_repo.get(product.id) выполниться не должна
#     assert not mock_product_repo.get.called, 'get (продукт) не должен быть вызван'
#     assert not mock_price_repo.save.called, 'save (цена) не должен быть вызван'
#     assert not mock_product_repo.save.called, 'save (продукт) не должен быть вызван'
#     assert not mock_user_repo.save.called, 'save (пользователь) не должен быть вызван'
