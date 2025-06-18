import pytest
import os

from core.price_cache import JSONPriceCache


@pytest.fixture
def cache_file(tmp_path):
    return str(tmp_path / 'prices.json')

@pytest.fixture
def price_cache(cache_file):
    return JSONPriceCache(cache_file=cache_file)

def test_load_empty_cache(price_cache):
    assert price_cache.cache == {}

def test_save_and_get_price(price_cache):
    price_cache.save_price('https://ozon.ru/product/1234567890', 900)
    assert price_cache.get_price('https://ozon.ru/product/1234567890') == 900
    assert os.path.exists(price_cache.cache_file)

def test_get_nonexist_price(price_cache):
    assert price_cache.get_price('https://ozon.ru/product/123') is None