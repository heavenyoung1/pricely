import pytest
import logging

from unittest.mock import Mock
from src.infrastructure.database.mappers import UserMapper
from src.domain.entities import User
from src.infrastructure.database.models import ORMUser

logger = logging.getLogger(__name__)

@pytest.mark.unit
def test_domain_to_orm(user):
    orm = UserMapper.domain_to_orm(user)
    assert isinstance(orm, ORMUser)
    assert orm.id == user.id
    assert orm.chat_id == user.chat_id

@pytest.mark.unit
def test_orm_to_domain(orm_user, orm_user_products):
    # Присваиваем user_products из фикстуры
    orm_user.user_products = orm_user_products
    
    domain = UserMapper.orm_to_domain(orm_user)
    logger.debug(f'USER ORM - {orm_user}')
    assert isinstance(domain, User)
    assert domain.id == orm_user.id
    assert len(domain.products) == 1
    assert 'p1' in domain.products