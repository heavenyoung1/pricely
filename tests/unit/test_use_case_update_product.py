import pytest

from src.application.use_cases.upd_product import UpdateProductPriceUseCase


@pytest.mark.unit
def test_upd_price_use_case_success(
    pure_mock_product_repo,
    pure_mock_price_repo,   
    product,
    price,
    price_second,
):
    pure_mock_product_repo.get.return_value = product
    pure_mock_price_repo.get.return_value = price

    use_case = UpdateProductPriceUseCase(
        product_repo=pure_mock_product_repo,
        price_repo=pure_mock_price_repo,
    )
    result = use_case.execute(product_id=product.id, price=price_second)
    # Проверяем, что продукт был получен
    pure_mock_product_repo.get.assert_called_once_with(product.id)

    # Проверяем, что цена сохранилась
    pure_mock_price_repo.save.assert_called_once_with(price_second)

    # Проверяем, что обновлённый продукт сохранился
    pure_mock_product_repo.save.assert_called_once_with(product)

    # И что продукт теперь указывает на новую цену
    assert product.price_id == price_second.id
    

    