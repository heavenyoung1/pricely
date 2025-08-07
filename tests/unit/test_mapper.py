import pytest
from pydantic import HttpUrl
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.infrastructure.database.models import ORMUser
from src.domain.entities import Product



@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    ORMUser.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    yield session
    session.close() 

@pytest.fixture
def product():
    return Product(
        id="prod1",
        user_id="user1",
        price_id=None,
        name="Test Product",
        link=HttpUrl("http://example.com"),
        image_url=HttpUrl("http://example.com/image.jpg"),
        rating=4.5,
        categories=["electronics", "gadgets"]
    )