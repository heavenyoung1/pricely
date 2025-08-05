from datetime import datetime

from src.domain.entities.product import Product
from domain.entities.price_claim import PriceStamp

from src.infrastructure.database.models.product import DBProduct
from src.infrastructure.database.models.price_stamp import DBPriceStamp

def test_save_one_product_integration(repo, db_session, product, price_stamp):
    repo.save_one_product(product, price_stamp)

    # Проверяем продукт
    db_product = db_session.query(DBProduct).filter_by(product_id='1804652778').first()
    assert db_product is not None
    assert db_product.name == 'Чаша для кальяна глиняная'
    assert db_product.price_with_card == 500

    # Проверяем клейм цены
    db_price_stamp = db_session.query(DBPriceStamp).filter_by(ID_stamp='stamp1').first()
    assert db_price_stamp is not None
    assert db_price_stamp.ID_product == '1804652778'
    assert db_price_stamp.price_with_card == 500

def test_save_one_product_update_integration(repo, db_session, product, price_stamp):
    db_product=product.to_orm()
    db_product.name = 'Старая чаша'
    db_product.price_with_card = 400
    db_session.add(db_product)
    db_session.commit()

    # Обновляем
    repo.save_one_product(product, price_stamp)

    # Проверяем, что продукт обновлен
    db_product = db_session.query(DBProduct).filter_by(product_id='1804652778').first()
    assert db_product.name == 'Чаша для кальяна глиняная'
    assert db_product.price_with_card == 500

    # Проверяем клейм
    db_price_stamp = db_session.query(DBPriceStamp).filter_by(ID_stamp='stamp1').first()
    assert db_price_stamp is not None

def test_save_few_products_integration(repo, db_session, product, price_stamps):
    product2 = Product(
        product_id='1804652779',
        user_id='0000000000',
        name='Чаша для кальяна керамическая',
        rating=4.8,
        price_with_card=600,
        price_without_card=661,
        previous_price_with_card=700,
        previous_price_without_card=700,
        price_default=999,
        link='https://www.ozon.ru/product/chasha-dlya-kalyana-keramicheskaya-1804652779/',
        url_image='https://ir.ozone.ru/s3/multimedia-1-9/wc1000/7352613514.jpg',
        category_product=['Товары для курения', 'Комплектующие'],
        last_timestamp=datetime(2025, 1, 1, 1, 2, 3),
    )

    products = [product, product2]

    repo.save_few_products(products, price_stamps)

    # Проверяем продукты
    db_products = db_session.query(DBProduct).all()
    assert len(db_products) == 2
    assert db_products[0].product_id == '1804652778'
    assert db_products[1].product_id == '1804652779'

    # Проверяем клеймо
    db_price_stamp = db_session.query(DBPriceStamp).filter_by(ID_stamp='stamp1').first()
    assert db_price_stamp is not None
