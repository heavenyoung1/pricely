from .uow_interface import UnitOfWork
from src.core.db_connection import get_session
from typing import Optional
from sqlalchemy.orm import Session
import logging

logger = logging.getLogger(__name__)

class SQLAlchemyUnitOfWork(UnitOfWork):
    '''Реализация Unit of Work для SQLAlchemy.'''
    def __init__(self, session_factory=None):
        '''
        Инициализация Unit of Work.
        
        Args:
            session_factory: Фабрика для создания сессий БД. Если не передана,
                           используется стандартная get_db_session.
        '''
        # Выбираем фабрику сессий: если передали свою - используем её,
        # если нет - используем стандартную функцию get_db_session
        # Это нужно для гибкости: в тестах можем передать другую фабрику
        self._session_factory = session_factory or get_session
        
        # Сессия БД. Пока None - создадим позже, когда войдем в контекст (with)
        # Optional[Session] означает "может быть Session, а может быть None"
        # Изначально None потому что сессия еще не создана
        self._session: Optional[Session] = None
        self._session_context = None

    @property
    def session(self) -> Optional[Session]:
        '''Публичный доступ к сессии SQLAlchemy.'''
        return self._session

    def __enter__(self):
        '''
        Вход в контекстный менеджер (начало блока 'with').
        Здесь создается сессия БД и инициализируются все репозитории.
        '''
        # 1. СОЗДАЕМ СЕССИЮ БД через фабрику
        # self._session_factory - это функция, которая умеет создавать сессии
        # Вызываем ее чтобы получить контекстный менеджер сессии
        self._session_context = self._session_factory()
        
        # 2. "ВХОДИМ" В СЕССИЮ - активируем контекстный менеджер
        # Метод __enter__() сессии выполняет начальную настройку:
        # - Подключается к БД
        # - Начинает транзакцию
        # - Возвращает объект сессии для работы
        self._session = self._session_context.__enter__()
        
        # 3. СОЗДАЕМ РЕПОЗИТОРИИ с общей сессией
        # Импорты здесь (а не в начале файла) чтобы избежать циклических импортов
        from src.infrastructure.database.repositories import (
            ProductRepositoryImpl,
            PriceRepositoryImpl,
            UserRepositoryImpl,
            UserProductsRepositoryImpl,
        )
        
        # 4. ИНИЦИАЛИЗИРУЕМ РЕПОЗИТОРИИ
        # Каждый репозиторий получает одну и ту же сессию БД
        # Это важно чтобы все операции были в одной транзакции
        self.product_repository = ProductRepositoryImpl(self._session)    # Репозиторий продуктов
        self.price_repository = PriceRepositoryImpl(self._session)        # Репозиторий цен
        self.user_repository = UserRepositoryImpl(self._session)          # Репозиторий пользователей
        self.user_products_repository = UserProductsRepositoryImpl(self._session)
        
        # 5. ЛОГГИРУЕМ успешную инициализацию
        logger.info('Unit of Work инициализирован с сессией и репозиториями')
        
        # 6. ВОЗВРАЩАЕМ СЕБЯ для использования в блоке 'with'
        # Теперь можно писать: with uow as u: u.products.get(...)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        '''
        Выход из контекстного менеджера (окончание блока 'with').
        Здесь обрабатывается завершение работы: коммит или откат транзакции.
        
        Args:
            exc_type: Тип исключения (если было исключение) или None (если все OK)
            exc_val: Объект исключения (содержит сообщение об ошибке)
            exc_tb: Traceback объект (информация о том, где произошла ошибка)
        '''
        try:
            # 1. ПРОВЕРЯЕМ БЫЛО ЛИ ИСКЛЮЧЕНИЕ
            if exc_type is not None:
                # 🚨 БЫЛА ОШИБКА в блоке with - откатываем транзакцию
                logger.warning(f'Исключение в Unit of Work: {exc_type.__name__}: {exc_val}')
                self.rollback()  # Откатываем все изменения в БД
            else:
                # ✅ ВСЕ OK - коммитим изменения
                self.commit()    # Сохраняем все изменения в БД
                
        finally:
            # 2. БЛOCK FINALLY - ВЫПОЛНЯЕТСЯ В ЛЮБОМ СЛУЧАЕ
            # Даже если выше произошла ошибка в commit() или rollback()
            if self._session_context:
                # 3. КОРРЕКТНО ЗАКРЫВАЕМ СЕССИЮ БД
                # Метод __exit__ сессии:
                # - Закрывает соединение с БД
                # - Освобождает ресурсы
                # - Обрабатывает исключения внутри сессии
                self._session_context.__exit__(exc_type, exc_val, exc_tb)
                
                # 4. ОЧИСТКА РЕСУРСОВ (опционально, но рекомендуется)
                self._session = None          # Убираем ссылку на сессию
                self._session_context = None  # Убираем ссылку на контекст
                
                logger.info("Unit of Work завершил работу, сессия закрыта")

    def commit(self):
        '''
        Фиксация всех изменений в БД.
        Сохраняет все выполненные операции (INSERT, UPDATE, DELETE) в базе данных.
        '''
    # 1. ПРОВЕРЯЕМ что сессия существует и активна
    # Это защита от случаев, когда commit() вызывают без активной сессии
        if self._session:
            try:
                # 2. ВЫПОЛНЯЕМ COMMIT - фиксируем изменения в БД
                # 💾 Этот момент когда все временные изменения становятся постоянными
                self._session.commit()
                logger.info('Unit of Work: транзакция зафиксирована, commit выполнен')
                
            except Exception as e:
                # 3. ОБРАБАТЫВАЕМ ОШИБКИ при коммите
                # 🚨 Если commit не удался (например, нарушение constraints БД)
                logger.error(f'Unit of Work: Транзакция не зафиксирована, commit не выполнен. Ошибка: {e}')
                
                # 4. ВЫПОЛНЯЕМ ROLLBACK при ошибке коммита
                # 🔄 Откатываем изменения чтобы не оставить транзакцию в подвешенном состоянии
                self.rollback()
                
                # 5. ВЫЗОВЕМ исключение 
                raise
        else:
            # 6. СЛУЧАЙ когда сессии нет (защита от неправильного использования)
            logger.warning('Unit of Work: Попытка commit без активной сессии БД')

    def rollback(self):
        '''
        Откат всех изменений в текущей транзакции.
        Отменяет все выполненные операции (INSERT, UPDATE, DELETE) с момента последнего commit.
        Возвращает базу данных в состояние, которое было до начала транзакции.
        '''
        # 1. ПРОВЕРЯЕМ что сессия существует и активна
        # 🛡️ Защита от случаев, когда rollback() вызывают без активной сессии
        if self._session:
            try:
                # 2. ВЫПОЛНЯЕМ ROLLBACK - откатываем изменения в БД
                # 🔄 Этот момент когда все временные изменения отменяются
                # База данных возвращается в состояние до начала транзакции
                self._session.rollback()
                logger.info('Unit of Work: транзакция откачена, rollback выполнен')
                
            except Exception as e:
                # 3. ОБРАБАТЫВАЕМ ОШИБКИ при rollback
                # 🚨 CRITICAL: Если rollback не удался - это серьезная проблема!
                # Это может означать проблемы с подключением к БД или corruption транзакции
                logger.error(f'Unit of Work: КРИТИЧЕСКАЯ ОШИБКА - не удалось выполнить rollback. Ошибка: {e}')
                
                # 4. ВЫЗЫВАЕМ исключение 
                raise
        else:
            # 5. СЛУЧАЙ когда сессии нет (защита от неправильного использования)
            logger.warning('Попытка rollback без активной сессии БД - нет транзакции для отката')