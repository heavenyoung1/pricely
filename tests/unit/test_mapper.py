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


