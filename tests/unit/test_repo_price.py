import pytest
import logging
#from pytest_mock import mocker
#from unittest.mock import MagicMock
from sqlalchemy.exc import SQLAlchemyError

from src.infrastructure.database.repositories import PriceRepositoryImpl, ProductRepositoryImpl
from src.infrastructure.database.mappers import PriceMapper
from src.infrastructure.database.models import ORMPrice
from src.domain.entities import Price



logger = logging.getLogger(__name__)

@pytest.mark.unit
def test_save_price_success(price_second, mock_session):
    '''
    Тестирование успешного сохранения цены через репозиторий.
    
    Args:
        price_second: Фикстура с доменным объектом Price для тестирования
        mock_session: Фикстура с мокированной сессией SQLAlchemy
    '''
    # Arrange (Подготовка)
    # Создаем экземпляр репозитория, передавая мокированную сессию
    repo = PriceRepositoryImpl(session=mock_session)
    
    # Act (Действие)
    # Вызываем метод save репозитория, передавая доменный объект цены
    repo.save(price=price_second)

    # Assert (Проверки)
    # 1. Проверяем, что метод merge сессии был вызван
    #    Это основной метод, который должен вызываться для сохранения/обновления
    assert mock_session.merge.called, "Метод merge сессии не был вызван"
    
    # 2. Извлекаем аргументы вызова метода merge
    # call_args[0] - кортеж позиционных аргументов
    # call_args[0][0] - первый позиционный аргумент (ORM объект)
    orm_obj = mock_session.merge.call_args[0][0]
    
    # Логируем полученный ORM объект для отладки
    logger.info(f"ORM объект, переданный в merge: {orm_obj}")
    
    # 3. Проверяем, что данные правильно смаппились из доменного объекта в ORM
    #    Сравниваем ID ORM объекта с ID доменного объекта
    assert orm_obj.id == price_second.id, (
        f"ID ORM объекта ({orm_obj.id}) не совпадает с ID доменного объекта ({price_second.id})"
    )
    
    # 4. Проверяем маппинг product_id
    assert orm_obj.product_id == price_second.product_id, (
        f"Product ID ORM объекта ({orm_obj.product_id}) "
        f"не совпадает с Product ID доменного объекта ({price_second.product_id})"
    )

def test_get_price_success(price_second, mock_session, orm_price):
    # Arrange (Подготовка)
    # Создаем экземпляр репозитория с мокированной сессией
    repo = PriceRepositoryImpl(session=mock_session)

    # Настраиваем мок сессии: при вызове get() возвращаем ORM объект
    mock_session.get.return_value = orm_price

    # Act (Действие)
    # Вызываем метод get репозитория для получения цены по ID
    result = repo.get(price_second.id)

    # Debug: Логируем для отладки
    logger.info(f'RESULT OBJECT ID: {result.id}')
    logger.info(f'EXPECTED PRICE ID: {price_second.id}')

    # Assert (Проверки)
    # 1. Проверяем, что возвращенный объект имеет правильные данные
    assert result.id == price_second.id
    assert result.product_id == price_second.product_id
    assert result.with_card == price_second.with_card
    assert result.without_card == price_second.without_card
    assert result.previous_with_card == price_second.previous_with_card
    assert result.previous_without_card == price_second.previous_without_card
    assert result.default == price_second.default
    assert result.claim == price_second.claim

    # 2. Проверяем, что session.get был вызван с ПРАВИЛЬНЫМИ аргументами:
    #    Первый аргумент: ORM класс (ORMPrice), второй аргумент: ID цены
    mock_session.get.assert_called_once_with(ORMPrice, price_second.id)
    
    assert result is not None, 'Метод get() вернул None'
    