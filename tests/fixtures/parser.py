import pytest

@pytest.fixture
def mock_parser(mocker):
    return mocker.Mock()