import pytest
from unittest.mock import ANY

from src.domain.exceptions import ProductNotFoundError, PriceUpdateError
from src.domain.entities import Price
from src.application.use_cases.upd_product import UpdateProductPriceUseCase


@pytest.mark.unit
def test_upd_price_use_case_success(
    pure_mock_product_repo,
    pure_mock_price_repo,
    product,
    price_created_first,
    price_after_checking,
    pure_mock_parser,
):
    pure_mock_product_repo.get.return_value = product
    pure_mock_price_repo.get_latest_for_product.return_value = price_created_first
    pure_mock_parser.check_product.return_value = {
        "price_with_card": price_after_checking.with_card,
        "price_without_card": price_after_checking.without_card,
    }

    use_case = UpdateProductPriceUseCase(
        product_repo=pure_mock_product_repo,
        price_repo=pure_mock_price_repo,
        parser=pure_mock_parser,
    )
    result = use_case.execute(product_id=product.id)

    # Проверяем, что продукт был получен
    pure_mock_product_repo.get.assert_called_once_with(product.id)

    # Проверяем, что последняя цена была получена для продукта
    pure_mock_price_repo.get_latest_for_product.assert_called_once_with(product.id)

    # Проверяем, что обновленная цена была сохранена, игнорируя created_at
    pure_mock_price_repo.save.assert_called_once_with(
        Price(
            id=None,
            product_id=price_after_checking.product_id,
            with_card=price_after_checking.with_card,
            without_card=price_after_checking.without_card,
            previous_with_card=price_after_checking.previous_with_card,
            previous_without_card=price_after_checking.previous_without_card,
            created_at=ANY,  # Игнорируем дату и время
        )
    )

    # Проверка флага изменения цены
    assert result["is_changed"] is True


@pytest.mark.unit
def test_upd_price_use_case_product_not_found(
    pure_mock_product_repo,
    pure_mock_price_repo,
    price_created_first,
    pure_mock_parser,
):
    # Настроим моки
    pure_mock_product_repo.get.return_value = None  # Продукт не найден

    use_case = UpdateProductPriceUseCase(
        product_repo=pure_mock_product_repo,
        price_repo=pure_mock_price_repo,
        parser=pure_mock_parser,
    )

    # Проверяем, что выбрасывается ошибка ProductNotFoundError
    with pytest.raises(ProductNotFoundError, match=f"Товар 1234567891 не найден"):
        use_case.execute(product_id="1234567891")


@pytest.mark.unit
def test_upd_price_use_case_parsing_error(
    pure_mock_product_repo,
    pure_mock_price_repo,
    product,
    pure_mock_parser,
):
    # Настроим моки
    pure_mock_product_repo.get.return_value = product
    pure_mock_price_repo.get_latest_for_product.return_value = None
    pure_mock_parser.check_product.side_effect = Exception(
        "Парсинг не удался"
    )  # Исключение при парсинге

    use_case = UpdateProductPriceUseCase(
        product_repo=pure_mock_product_repo,
        price_repo=pure_mock_price_repo,
        parser=pure_mock_parser,
    )

    # Проверяем, что выбрасывается ошибка PriceUpdateError
    with pytest.raises(
        PriceUpdateError, match=f"Ошибка при обновлении цены товара {product.id}"
    ):
        use_case.execute(product_id=product.id)


@pytest.mark.unit
def test_upd_price_use_case_no_change(
    pure_mock_product_repo,
    pure_mock_price_repo,
    product,
    price_created_first,
    pure_mock_parser,
):
    # Настроим моки
    pure_mock_product_repo.get.return_value = product
    pure_mock_price_repo.get_latest_for_product.return_value = price_created_first
    pure_mock_parser.check_product.return_value = {
        "price_with_card": price_created_first.with_card,
        "price_without_card": price_created_first.without_card,
    }  # Цена не изменилась

    use_case = UpdateProductPriceUseCase(
        product_repo=pure_mock_product_repo,
        price_repo=pure_mock_price_repo,
        parser=pure_mock_parser,
    )
    result = use_case.execute(product_id=product.id)

    # Проверяем, что флаг изменения цены установлен в False
    assert result["is_changed"] is False


@pytest.mark.unit
def test_upd_price_use_case_unexpected_error(
    pure_mock_product_repo,
    pure_mock_price_repo,
    product,
    price_created_first,
    pure_mock_parser,
):
    # Настроим моки
    pure_mock_product_repo.get.return_value = product
    pure_mock_price_repo.get_latest_for_product.return_value = price_created_first
    pure_mock_parser.check_product.return_value = {
        "price_with_card": 1950,
        "price_without_card": 1900,
    }

    # Симулируем ошибку в репозитории при сохранении
    pure_mock_price_repo.save.side_effect = Exception(
        "Неизвестная ошибка при сохранении"
    )

    use_case = UpdateProductPriceUseCase(
        product_repo=pure_mock_product_repo,
        price_repo=pure_mock_price_repo,
        parser=pure_mock_parser,
    )

    # Проверяем, что выбрасывается ошибка PriceUpdateError
    with pytest.raises(PriceUpdateError, match="Ошибка при обновлении цены товара"):
        use_case.execute(product_id=product.id)
