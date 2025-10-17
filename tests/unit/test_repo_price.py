import pytest
import logging

from src.infrastructure.database.repositories import PriceRepositoryImpl
from src.infrastructure.database.models import ORMPrice


logger = logging.getLogger(__name__)

@pytest.mark.unit
def test_save_price_success(price_created_first, mock_session):
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
    repo.save(price=price_created_first)

    # Assert (Проверки)
    # 1. Проверяем, что метод merge сессии был вызван
    #    Это основной метод, который должен вызываться для сохранения/обновления
    assert mock_session.merge.called, 'Метод merge сессии не был вызван'
    
    # 2. Извлекаем аргументы вызова метода merge
    # call_args[0] - кортеж позиционных аргументов
    # call_args[0][0] - первый позиционный аргумент (ORM объект)
    orm_obj = mock_session.merge.call_args[0][0]
    
    # Логируем полученный ORM объект для отладки
    logger.info(f'ORM объект, переданный в merge: {orm_obj}')
    
    # 3. Проверяем, что данные правильно смаппились из доменного объекта в ORM
    #    Сравниваем ID ORM объекта с ID доменного объекта
    assert orm_obj.id == price_created_first.id, (
        f'ID ORM объекта ({orm_obj.id}) не совпадает с ID доменного объекта ({price_created_first.id})'
    )
    
    # 4. Проверяем маппинг product_id
    assert orm_obj.product_id == price_created_first.product_id, (
        f'Product ID ORM объекта ({orm_obj.product_id}) '
        f'не совпадает с Product ID доменного объекта ({price_created_first.product_id})'
    )

@pytest.mark.unit
def test_save_price_error(price_created_first, mock_session):
    '''
    Тестирование ошибки при сохранении цены через репозиторий.
    Проверка, что в случае ошибки метод raise исключение.
    '''
    # Настроим мок сессии, чтобы при вызове метода merge возникала ошибка
    mock_session.merge.side_effect = Exception('Ошибка при сохранении')
    
    repo = PriceRepositoryImpl(session=mock_session)
    
    # Ожидаем, что при вызове save будет выброшено исключение
    with pytest.raises(Exception):
        repo.save(price=price_created_first)
    
    # Проверяем, что метод merge был вызван
    mock_session.merge.assert_called_once()

@pytest.mark.unit
def test_get_price_success(price_created_first, mock_session, orm_price_created_first):
    # Arrange (Подготовка)
    # Создаем экземпляр репозитория с мокированной сессией
    repo = PriceRepositoryImpl(session=mock_session)

    # Настраиваем мок сессии: при вызове get() возвращаем ORM объект
    mock_session.get.return_value = orm_price_created_first

    # Act (Действие)
    # Вызываем метод get репозитория для получения цены по ID
    result = repo.get(price_created_first.id)

    # Debug: Логируем для отладки
    logger.info(f'RESULT OBJECT ID: {result.id}')
    logger.info(f'EXPECTED PRICE ID: {price_created_first.id}')

    # Assert (Проверки)
    assert result.product_id == price_created_first.product_id

    # 2. Проверяем, что session.get был вызван с ПРАВИЛЬНЫМИ аргументами:
    #    Первый аргумент: ORM класс (ORMPrice), второй аргумент: ID цены
    mock_session.get.assert_called_once_with(ORMPrice, price_created_first.id)
    
    assert result is not None, 'Метод get() вернул None'
    
@pytest.mark.unit
def test_get_all_prices_by_product(mock_session, price_after_checking, orm_price_created_checking):
    repo = PriceRepositoryImpl(session=mock_session)

    # подсовываем ORM объект как результат запроса
    mock_session.query.return_value.filter_by.return_value.all.return_value = [orm_price_created_checking]

    result = repo.get_all_prices_by_product(product_id=price_after_checking.product_id)

    # проверки
    assert len(result) == 1

    # проверяем, что репозиторий ходил именно в таблицу prices
    mock_session.query.assert_called_once_with(ORMPrice)

@pytest.mark.unit
def test_delete_price_success(mock_session, orm_price_created_first):
    '''
    Тестирование успешного удаления цены через репозиторий.
    '''
    # Настроим мок сессии для получения ORM объекта
    mock_session.get.return_value = orm_price_created_first

    repo = PriceRepositoryImpl(session=mock_session)

    # Выполняем удаление
    result = repo.delete(price_id=orm_price_created_first.id)

    # Проверяем, что товар был удален
    assert result is True
    
    # Проверяем, что метод delete был вызван
    mock_session.get.assert_called_once_with(ORMPrice, orm_price_created_first.id)
    mock_session.delete.assert_called_once_with(orm_price_created_first)
    
@pytest.mark.unit
def test_delete_price_not_found(mock_session):
    '''
    Тестирование удаления цены, если товар не найден.
    '''
    # Настроим мок сессии так, что товар не будет найден
    mock_session.get.return_value = None

    repo = PriceRepositoryImpl(session=mock_session)

    # Выполняем удаление
    result = repo.delete(price_id='NOTEXIST_ID')

    # Проверяем, что товар не был удален
    assert result is False

    # Проверяем, что метод get был вызван с правильным ID
    mock_session.get.assert_called_once_with(ORMPrice, 'NOTEXIST_ID')
    
@pytest.mark.unit
def test_get_all_prices_no_prices(mock_session, price_after_checking):
    '''
    Тестирование получения всех цен для продукта, если нет цен в базе данных.
    '''
    repo = PriceRepositoryImpl(session=mock_session)

    # Настроим мок сессии для возврата пустого списка цен
    mock_session.query.return_value.filter_by.return_value.all.return_value = []

    result = repo.get_all_prices_by_product(product_id=price_after_checking.product_id)

    # Проверяем, что вернулся пустой список
    assert len(result) == 0

    # Проверяем, что метод query был вызван
    mock_session.query.assert_called_once_with(ORMPrice)