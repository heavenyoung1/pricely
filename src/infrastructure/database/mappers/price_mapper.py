from src.domain.entities import Price
from src.application.dto import PriceDTO
from src.infrastructure.database.models import ORMPrice
from deprecated import deprecated


class PriceMapper:
    '''
    Маппер для преобразования между объектами домена и ORM.

    Этот класс содержит методы для преобразования данных между различными слоями:
    - Domain
    - ORM (Object-Relational Mapping)
    '''
    
    @staticmethod
    @deprecated(reason='Этот метод скоро будет удален. Используйте новый метод для преобразования.')
    def dto_to_domain(dto: PriceDTO) -> Price:
        '''
        Преобразует объект PriceDTO в объект Price (доменная модель).

        :param dto: Объект типа PriceDTO.
        :return: Объект типа Price (доменная модель).
        '''
        return Price(
            id=dto.id,  # теперь может быть None
            product_id=dto.product_id,
            with_card=dto.with_card,
            without_card=dto.without_card,
            previous_with_card=dto.previous_with_card,
            previous_without_card=dto.previous_without_card,
            created_at=dto.created_at,
        )

    @staticmethod
    @deprecated(reason='Этот метод скоро будет удален. Используйте новый метод для преобразования.')
    def domain_to_dto(domain: Price) -> PriceDTO:
        '''
        Преобразует объект Price (доменная модель) в объект PriceDTO (Data Transfer Object).

        :param domain: Объект типа Price (доменная модель).
        :return: Объект типа PriceDTO.
        '''
        return PriceDTO(
            id=domain.id,  # None до сохранения в БД → норм
            product_id=domain.product_id,
            with_card=domain.with_card,
            without_card=domain.without_card,
            previous_with_card=domain.previous_with_card,
            previous_without_card=domain.previous_without_card,
            created_at=domain.created_at,
        )

    @staticmethod
    def domain_to_orm(domain: Price) -> ORMPrice:
        '''
        Преобразует объект Price (доменная модель) в объект ORMPrice (ORM модель для работы с БД).

        :param domain: Объект типа Price (доменная модель).
        :return: Объект типа ORMPrice для сохранения в базе данных.
        '''
        return ORMPrice(
            # id не задаём руками, автоинкремент!!!
            product_id=domain.product_id,
            with_card=domain.with_card,
            without_card=domain.without_card,
            previous_with_card=domain.previous_with_card,
            previous_without_card=domain.previous_without_card,
            created_at=domain.created_at,
        )

    @staticmethod
    def orm_to_domain(orm: ORMPrice) -> Price:
        '''
        Преобразует объект ORMPrice (ORM модель) в объект Price (доменная модель).

        :param orm: Объект типа ORMPrice.
        :return: Объект типа Price (доменная модель).
        '''
        return Price(
            id=orm.id,
            product_id=orm.product_id,
            with_card=orm.with_card,
            without_card=orm.without_card,
            previous_with_card=orm.previous_with_card,
            previous_without_card=orm.previous_without_card,
            created_at=orm.created_at,
        )