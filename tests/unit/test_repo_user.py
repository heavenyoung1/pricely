import pytest

from src.infrastructure.database.models import ORMUser
from src.domain.entities import User
from src.infrastructure.database.repositories import UserRepositoryImpl

import logging
logger = logging.getLogger(__name__)

@pytest.mark.unit
def test_save_user_success(user, mock_session):
    repo = UserRepositoryImpl(session=mock_session)
    repo.save(user)
    mock_session.merge.assert_called_once()

@pytest.mark.unit  
def test_get_user_found(mock_session, orm_user, user):
    repo = UserRepositoryImpl(session=mock_session)
    mock_session.get.return_value = orm_user
    result = repo.get(user_id=user.id)
    assert result.id == user.id
    mock_session.get.assert_called_once_with(ORMUser, user.id)

@pytest.mark.unit  
def test_get_user_not_found(mock_session):
    repo = UserRepositoryImpl(session=mock_session)
    mock_session.get.return_value = None
    result = repo.get(user_id='NOTEXIST_ID')
    assert result is None
    mock_session.get.assert_called_once_with(ORMUser, 'NOTEXIST_ID')

@pytest.mark.unit  
def test_delete_user_found(mock_session, orm_user, user):
    repo = UserRepositoryImpl(session=mock_session)
    mock_session.get.return_value = orm_user
    repo.delete(user_id=user.id)
    mock_session.get.assert_called_once_with(ORMUser, user.id)
    mock_session.delete.assert_called_once_with(orm_user)

@pytest.mark.unit  
def test_delete_user_not_found(mock_session):
    repo = UserRepositoryImpl(session=mock_session)
    mock_session.get.return_value = None
    
    repo.delete('NOTEXIST_ID')
    
    mock_session.get.assert_called_once_with(ORMUser, 'NOTEXIST_ID')
    mock_session.delete.assert_not_called()