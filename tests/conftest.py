import pytest
import logging
import sys
import json
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from unittest.mock import MagicMock
from pydantic import HttpUrl


pytest_plugins = [
    'fixtures.database',
    'fixtures.product',
    'fixtures.price', 
    'fixtures.user',
    'fixtures.repositories',
    'fixtures.service',
    'fixtures.parser',
]

@pytest.fixture(autouse=True)
def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        stream=sys.stdout
    )


