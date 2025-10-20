import pytest
from src.infrastructure.services import ProductService
from src.infrastructure.parsers import OzonParser

@pytest.fixture
def product_service(mock_uow):
    '''Фикстура для создания сервиса ProductService.'''
    return ProductService(uow_factory=mock_uow, parser=OzonParser())