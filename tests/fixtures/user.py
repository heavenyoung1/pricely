import pytest

from src.application.dto import UserDTO
from src.domain.entities import User
from src.infrastructure.database.models import ORMUser


@pytest.fixture
def user_dto():
    '''Фикстура тестового User DTO'''
    return UserDTO(
        id='u1',
        username='test_user',
        chat_id='12345',
        products=['p1', 'p2']
    )

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
def orm_user(session, orm_product):
    '''Фикстура тестового ORM User'''
    user = ORMUser(
        id='u1',
        username='test_user',
        chat_id='12345',
        #products=['p1', 'p2'] # НЕ передаем products в конструктор!
    )
    session.add(user)
    session.flush()
    user.products = [orm_product]
    session.commit()
    return user
