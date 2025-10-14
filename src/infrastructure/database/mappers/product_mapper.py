from pydantic import HttpUrl
from deprecated import deprecated

from src.domain.entities import Product
from src.application.dto import ProductDTO
from src.infrastructure.database.models import ORMProduct
from src.infrastructure.database.mappers.price_mapper import PriceMapper


class ProductMapper:
    '''
    Маппер для преобразования между объектами Product и ORMProduct.

    Этот класс содержит методы для преобразования данных между различными слоями:
    - Domain
    - ORM (Object-Relational Mapping)
    '''

    @staticmethod
    @deprecated(reason='Этот метод скоро будет удален. Используйте новый метод для преобразования.')
    def dto_to_domain(dto: ProductDTO) -> Product:
        '''
        Преобразует объект ProductDTO в объект Product (доменная модель).

        :param dto: Объект типа ProductDTO.
        :return: Объект типа Product (доменная модель).
        '''
        return Product(
            id=dto.id,
            user_id=dto.user_id,
            name=dto.name,
            link=str(dto.link),
            image_url=str(dto.image_url),
            rating=dto.rating,
            categories=dto.categories,
        )

    @staticmethod
    @deprecated(reason='Этот метод скоро будет удален. Используйте новый метод для преобразования.')
    def domain_to_dto(domain: Product) -> ProductDTO:
        '''
        Преобразует объект Product (доменная модель) в объект ProductDTO (Data Transfer Object).

        :param domain: Объект типа Product (доменная модель).
        :return: Объект типа ProductDTO.
        '''
        return ProductDTO(
            id=domain.id,
            user_id=domain.user_id,
            name=domain.name,
            link=HttpUrl(domain.link),
            image_url=HttpUrl(domain.image_url),
            rating=domain.rating,
            categories=domain.categories,
        )

    @staticmethod
    def domain_to_orm(domain: Product) -> ORMProduct:
        '''
        Преобразует объект Product (доменная модель) в объект ORMProduct (ORM модель для работы с БД).

        :param domain: Объект типа Product (доменная модель).
        :return: Объект типа ORMProduct для сохранения в базе данных.
        '''
        return ORMProduct(
            id=domain.id,
            name=domain.name,
            link=domain.link,
            image_url=domain.image_url,
            rating=domain.rating,
            categories=domain.categories,
        )

    @staticmethod
    def orm_to_domain(orm: ORMProduct) -> Product:
        '''
        Преобразует объект ORMProduct (ORM модель) в объект Product (доменная модель).

        :param orm: Объект типа ORMProduct.
        :return: Объект типа Product (доменная модель).
        '''
        return Product(
            id=orm.id,
            user_id='',  # Убрано, так как нет в ORM
            name=orm.name,
            link=orm.link,
            image_url=orm.image_url,
            rating=orm.rating,
            categories=orm.categories,
            prices=[PriceMapper.orm_to_domain(p) for p in orm.prices] if orm.prices else [],
        )