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