import pytest

from src.application.use_cases.delete_product import DeleteProductUseCase
from src.domain.exceptions import ProductNotExistingDataBase, ProductDeletingError


@pytest.mark.unit
def test_delete_product_use_case_success(
    pure_mock_product_repo,
    pure_mock_price_repo,
    pure_mock_user_repo,
    product,
    price_created_first,
    price_after_checking,
    user,
):
    # Настраиваем моки
    pure_mock_product_repo.get.return_value = product
    pure_mock_price_repo.get_all_prices_by_product.return_value = [
        price_created_first,
        price_after_checking,
    ]
    # pure_mock_price_repo.get_latest_for_product.return_value = price
    pure_mock_user_repo.get.return_value = user

    # Добавляем товар в список продуктов пользователя для успешного вызова save
    user.products.append(product.id)

    use_case = DeleteProductUseCase(
        product_repo=pure_mock_product_repo,
        price_repo=pure_mock_price_repo,
        user_repo=pure_mock_user_repo,
    )

    use_case.execute(product_id=product.id)

    # Проверяем вызовы
    pure_mock_price_repo.delete_all_prices_for_product.assert_called_once_with(
        product.id
    )
    pure_mock_product_repo.delete.assert_called_once_with(product.id)
    pure_mock_user_repo.get.assert_called_once_with(product.user_id)
    pure_mock_user_repo.save.assert_called_once_with(user)
    assert product.id not in user.products


@pytest.mark.unit
def test_delete_product_use_case_unsuccess_notexist_in_db(
    pure_mock_product_repo,
    pure_mock_price_repo,
    pure_mock_user_repo,
    product,
):
    pure_mock_product_repo.get.return_value = None

    use_case = DeleteProductUseCase(
        product_repo=pure_mock_product_repo,
        price_repo=pure_mock_price_repo,
        user_repo=pure_mock_user_repo,
    )

    with pytest.raises(
        ProductNotExistingDataBase, match=f"Товар {product.id} не существует в БД!"
    ):
        use_case.execute(product_id=product.id)


@pytest.mark.unit
def test_delete_product_use_case_fails(
    pure_mock_product_repo,
    pure_mock_price_repo,
    pure_mock_user_repo,
    product,
    price_created_first,
    price_after_checking,
    user,
):
    # Настроим моки
    pure_mock_product_repo.get.return_value = product
    pure_mock_price_repo.get_all_prices_by_product.return_value = [
        price_created_first,
        price_after_checking,
    ]
    pure_mock_user_repo.get.return_value = user

    # Симулируем ошибку при удалении товара в репозитории
    pure_mock_product_repo.delete.side_effect = Exception("Ошибка удаления товара")

    # Act & Assert
    use_case = DeleteProductUseCase(
        product_repo=pure_mock_product_repo,
        price_repo=pure_mock_price_repo,
        user_repo=pure_mock_user_repo,
    )

    # Проверка на выброс ошибки
    with pytest.raises(ProductDeletingError, match="Ошибка удаления товара"):
        use_case.execute(product_id=product.id)

    # Проверяем, что другие методы не были вызваны
    # 🧪🧪🧪(ТИКЕТ #26) СТРОКА НИЖЕ НЕ ДОЛЖНА ВЫПОЛНЯТЬСЯ
    # pure_mock_price_repo.delete_all_prices_for_product.assert_not_called()
    pure_mock_product_repo.save.assert_not_called()
    pure_mock_user_repo.save.assert_not_called()
