from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    '''
    Базовый класс для всех ORM моделей.

    Этот класс используется в качестве родительского для всех ORM моделей,
    обеспечивая базовую функциональность для работы с базой данных через SQLAlchemy.
    '''
    pass