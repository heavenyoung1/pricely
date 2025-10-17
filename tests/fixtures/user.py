import pytest

from src.domain.entities import User
from src.infrastructure.database.models import ORMUser

@pytest.fixture
def user():
    '''Фикстура тестового доменного User'''
    return User(
        id='635777007',
        username='Ololoshka',
        chat_id='635777007',
        #products=['816992280', '1522830591']
    )

@pytest.fixture
def orm_user():
    '''Фикстура тестового ORM User'''
    return ORMUser(
        id='635777007',
        username='Ololoshka',
        chat_id='635777007',
    )