import pytest
import logging

from unittest.mock import Mock
from src.infrastructure.database.mappers import UserMapper
from src.domain.entities import User
from src.infrastructure.database.models import ORMUser

logger = logging.getLogger(__name__)

@pytest.mark.unit
def test_domain_to_orm(user: User):
    '''
    Тестирование преобразования доменной модели User в ORM модель ORMUser.
    '''
    orm_user = UserMapper.domain_to_orm(user)
    assert isinstance(orm_user, ORMUser)  # Проверяем тип данных

    # Проверяем, что поля соответствуют между доменной моделью и ORM моделью
    assert_users_equal(orm_user, user)


@pytest.mark.unit
def test_orm_to_domain(orm_user: ORMUser):
    '''
    Тестирование преобразования ORM модели ORMUser в доменную модель User.
    '''
    domain_user = UserMapper.orm_to_domain(orm_user)
    assert isinstance(domain_user, User)  # Проверяем тип данных

    # Проверяем, что поля соответствуют между ORM моделью и доменной моделью
    assert_users_equal(orm_user, domain_user)

    # Универсальная функция для сравнения объектов User и ORMUser
def assert_users_equal(orm_user, domain_user):
    '''
    Универсальная функция для сравнения объектов User и ORMUser.
    Проверяет, что все поля соответствуют друг другу.

    Аргументы:
        orm_user (ORMUser): Объект ORM (ORMUser), который нужно проверить.
        domain_user (User): Объект доменной модели (User), с которым будем сравнивать.
    '''
    assert orm_user.id == domain_user.id, f'Несоответствие ID: {orm_user.id} != {domain_user.id}'
    assert orm_user.username == domain_user.username, f'Несоответствие имени пользователя: {orm_user.username} != {domain_user.username}'
    assert orm_user.chat_id == domain_user.chat_id, f'Несоответствие chat_id: {orm_user.chat_id} != {domain_user.chat_id}'
    #assert orm_user.user_products == domain_user.products, f'Несоответствие продуктов: {orm_user.user_products} != {domain_user.products}'
