import json

from src.infrastructure.mappers import ProductMapper, PriceMapper, UserMapper

def test_product_mapper_to_orm(product):
    orm_product = ProductMapper.to_orm(product)
    assert orm_product.id == product.id
    assert orm_product.user_id == product.user_id
    assert orm_product.price_id == product.price_id
    assert orm_product.name == product.name
    assert orm_product.link == str(product.link)
    assert orm_product.image_url == str(product.image_url)
    assert orm_product.rating == product.rating
    assert orm_product.categories == json.dumps(product.categories)

def test_price_mapper_to_orm(price, session):
    orm_price = PriceMapper.to_orm(price)
    assert orm_price.id == price.id
    assert orm_price.product_id == price.product_id
    assert orm_price.with_card == price.with_card
    assert orm_price.without_card == price.without_card
    assert orm_price.previous_with_card == price.previous_with_card
    assert orm_price.previous_without_card == price.previous_without_card
    assert orm_price.default == price.default
    assert orm_price.date_claim == price.claim

