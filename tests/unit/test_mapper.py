from sqlalchemy import create_engine, Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

Base = declarative_base()

class ORMProduct(Base):
    product_id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey('users.user_id'))
    name = Column(String)
    link = Column(String)
    image_url = Column(String)
    rating = Column(String)
    categories = Column(String)
    user = Column(String)
    price_claims = Column(String)

class ORMPrice(Base):
    __tablename__ = "prices"
    id = Column(String, primary_key=True)
    with_card = Column(Integer)
    without_card = Column(Integer)
    previous_with_card = Column(Integer, nullable=True)
    previous_without_card = Column(Integer, nullable=True)
    default = Column(Integer)
    price_claim_id = Column(String, ForeignKey("price_claims.claim_id"))