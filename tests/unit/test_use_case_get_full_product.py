import pytest
import json
from src.application.use_cases.get_full_product import GetFullProductUseCase
from src.domain.entities import Product, Price, User
from src.infrastructure.mappers import ProductMapper
from src.infrastructure.database.models import ORMUser

def test_get_full_product_use_case_success(
        mock_product_repo, 
        mock_price_repo, 
        mock_user_repo, 
        product, 
        price, 
        user,
    ):
    '''Успешное получение полной информации о товаре.'''

    # Настраиваем моки: продукт существует
    mock_product_repo.get.return_value = product
    mock_price_repo.get.return_value = price
    mock_user_repo.get.return_value = user

    # Создаём use case
    use_case = GetFullProductUseCase(
        product_repo=mock_product_repo,
        price_repo=mock_price_repo,
        user_repo=mock_user_repo,
    )

    result = use_case.execute(product_id=product.id)

    assert result == {'product': product, 'price': price, 'user': user} 
    mock_product_repo.get.assert_called_once_with(product.id)
    mock_price_repo.get.assert_called_once_with(product.price_id)
    mock_user_repo.get.assert_called_once_with(product.user_id)
    
