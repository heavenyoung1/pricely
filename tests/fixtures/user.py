import pytest

from src.domain.entities import User
from src.infrastructure.database.models import ORMUser

@pytest.fixture
def user():
    '''Фикстура тестового доменного User'''
    return User(
        id='u1',
        username='test_user',
        chat_id='12345',
        products=['p1', 'p2']
    )

@pytest.fixture
def orm_user():
    '''Фикстура тестового ORM User'''
    return ORMUser(
        id='u1',
        username='test_user',
        chat_id='12345',
    )
