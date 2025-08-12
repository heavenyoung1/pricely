from datetime import datetime
from src.domain.entities import Product, Price, User

def test_product_structure(product):
    '''Проверяем структуру и типы данных продукта'''
    assert isinstance(product, Product)
    assert len(product.id) == 10
    assert len(product.user_id) == 9
    assert product.name == 'Кофе молотый DeLonghi'
    assert 0 <= product.rating <= 5
    assert isinstance(product.categories, list)
    assert len(product.categories) > 0
    assert all(isinstance(cat, str) for cat in product.categories)

def test_price_logic(price):
    '''Проверяем бизнес-логику цен'''
    assert price.with_card < price.without_card, 'Цена по карте должна быть ниже'
    assert price.default > price.without_card, 'Базовая цена должна быть выше'
    assert isinstance(price.claim, datetime), 'Дата должна быть datetime'

def test_user_relations(user, product):
    '''Проверяем связи между сущностями'''
    assert user.id == product.user_id
    assert product.id in eval(user.products)  # Осторожно с eval, лучше использовать json.loads
