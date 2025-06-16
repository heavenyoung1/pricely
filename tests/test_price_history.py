from datetime import datetime

import pytest
import logging

from core.price_history import PriceHistory


@pytest.fixture
def price_history():
    return PriceHistory(
        id='1234567890',
        url='https://ozon.ru/product/1234567890',
        history=[
            (950, datetime(2025, 6, 13))
        ]
    )

def test_price_history_initialization(price_history):
    assert price_history.id == "1234567890"
    assert price_history.url == "https://ozon.ru/product/1234567890"
    assert price_history.history == [(950, datetime(2025, 6, 13))]

def test_add_price(price_history):
    price_history.add_price(930)
    assert len(price_history.history) == 2
    assert price_history.history[-1][0] == 930

def test_get_last_price(price_history):
    assert price_history.get_last_price() == 950

def test_get_last_price_empty():
    empty_history = PriceHistory(
        id="1234567890",
        url="https://ozon.ru/product/1234567890",
        history=[]
    )
    assert empty_history.get_last_price() is None