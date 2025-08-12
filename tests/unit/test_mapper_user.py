import pytest
from src.infrastructure.mappers import UserMapper
from src.interfaces.dto import UserDTO
from src.domain.entities import User
from src.infrastructure.database.models import ORMUser


def test_dto_to_domain(user_dto):
    domain = UserMapper.dto_to_domain(user_dto)
    assert isinstance(domain, User)
    assert domain.id == user_dto.id
    assert domain.products == user_dto.products

def test_domain_to_dto(user):
    dto = UserMapper.domain_to_dto(user)
    assert isinstance(dto, UserDTO)
    assert dto.id == user.id
    assert dto.username == user.username

def test_domain_to_orm(user):
    orm = UserMapper.domain_to_orm(user)
    assert isinstance(orm, ORMUser)
    assert orm.id == user.id
    assert orm.chat_id == user.chat_id

def test_orm_to_domain(orm_user):
    domain = UserMapper.orm_to_domain(orm_user)
    assert isinstance(domain, User)
    assert domain.id == orm_user.id
    assert domain.products == orm_user.products