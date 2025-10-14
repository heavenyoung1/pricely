from src.core.uow import SQLAlchemyUnitOfWork
from typing import Callable, Any, Optional
import functools
import logging

logger = logging.getLogger(__name__)

def with_uow(commit: bool = False, uow_class: type = SQLAlchemyUnitOfWork):
    '''
    Декоратор для работы с Unit of Work (UoW) паттерном.
    
    Args:
        commit (bool): Флаг указывающий, нужно ли выполнять commit транзакции. 
                      Если False - выполняется rollback. По умолчанию False.
        uow_class (Type): Класс Unit of Work для использования. 
                         По умолчанию SQLAlchemyUnitOfWork.
    
    Returns:
        Callable: Декорированная функция с поддержкой UoW.
    
    Example:
        @with_uow(commit=True)
        def create_user(uow, user_data):
            # работа с базой через uow
            return user
    '''
    def decorator(func: Callable) -> Callable:
        '''
        Внутренний декоратор, который оборачивает целевую функцию.
        
        Args:
            func (Callable): Функция, которую нужно декорировать.
                            Первым аргументом должна принимать uow.
        
        Returns:
            Callable: Обернутая функция с UoW контекстом.
        '''
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs) -> Any:
            '''
            Обертка функции, которая управляет жизненным циклом UoW.
            
            Returns:
                Any: Результат выполнения оригинальной функции.
            
            Raises:
                Exception: Любое исключение, возникшее в декорируемой функции.
            '''
            # Создаем экземпляр Unit of Work
            # uow = uow_class()
            # ------------- выше старое решение, потом удалить!!! --------- #
            # Используем фабрику UOW из объекта self
            # Это позволяет тестам передавать свой UOW через фабрику
            uow = self.uow_factory()
            
            try:
                # Входим в контекстный менеджер UoW
                # Контекстный менеджер автоматически управляет сессией/транзакцией
                with uow:
                    # Устанавливаем self.uow для доступа внутри функции
                    self.uow = uow
                    # Вызываем оригинальную функцию, передавая uow первым аргументом
                    # uow будет автоматически передан в функцию как первый позиционный аргумент
                    result = func(self, *args, **kwargs) # Убрал передачу аргумента uow 
                    
                    # Логика управления транзакцией в зависимости от флага commit
                    if commit:
                        # Если commit=True - логируем и позволяем контекстному менеджеру
                        # выполнить commit при успешном завершении
                        logger.info(f'Функция {func.__name__}: выполняется commit транзакции')
                        uow.commit()  # Явный commit
                        # Примечание: commit обычно выполняется в методе __exit__ 
                        # контекстного менеджера при успешном завершении блока with
                    else:
                        # Если commit=False - явно выполняем rollback
                        # Это предотвращает случайное сохранение изменений
                        logger.info(f'Функция {func.__name__}: commit пропущен, выполняется rollback')
                        # Явный rollback отменяет все изменения в текущей транзакции
                        uow.rollback()
                    
                    # Возвращаем результат оригинальной функции
                    return result
                    
            except Exception as e:
                # Логируем любые ошибки, возникшие в декорируемой функции
                logger.error(f'Ошибка в функции {func.__name__}: {str(e)}')
                
                # Примечание: контекстный менеджер UoW автоматически выполнит rollback
                # в своем методе __exit__ при возникновении исключения
                # Это обеспечивает атомарность операций - либо все изменения применяются,
                # либо ни одно не применяется
                
                # Пробрасываем исключение дальше для обработки вызывающей стороной
                raise
            finally:
                # Очищаем self.uow после завершения
                self.uow = None
                
        return wrapper  # Возвращаем обернутую функцию
        
    return decorator  # Возвращаем декоратор