from src.interfaces.dto.product_dto import ProductCreateDTO, PriceCreateDTO, UserCreateDTO
from src.application.services.product_service import ProductService
import logging
from interfaces.dto.dto_to_domain import (
    product_dto_to_entity, 
    price_dto_to_entity, 
    user_dto_to_entity
    )

from tests.unit.fake_uow import FakeUnitOfWork

logger = logging.getLogger(__name__)

def test_full_flow():
    uow = FakeUnitOfWork()
    service = ProductService(lambda: uow)  # теперь сервис использует тот же самый uow
    logger.debug('Инициализирован ProductService')

    # 1. DTO → Entity
    product_dto = ProductCreateDTO(
        id='p1',
        user_id='u1',
        name='Товар 1',
        link='https://example.com/product1',
        image_url='https://example.com/img1.jpg',
        rating=4.8,
        categories=['cat1', 'cat2']
    ) 
    
    price_dto = PriceCreateDTO(
        id='pr1',
        product_id='p1',
        with_card=100,
        without_card=120,
        previous_with_card=110,
        previous_without_card=130,
        default=100,
        claim='2025-08-09T12:00:00'
    )
    user_dto = UserCreateDTO(
        id='u1',
        username='test_user',
        chat_id='12345',
        products=[]
    )
    logger.debug('DTO преобразованы в Entity')

    product_entity = product_dto_to_entity(product_dto)
    price_entity = price_dto_to_entity(price_dto)
    user_entity = user_dto_to_entity(user_dto)

    # 2. ENTITY → UseCase → Service → Repo
    service.create_product_with_price(product_entity, price_entity, user_entity)

    #uow = uow_factory()

    print('Products in repo:', uow.product_repository()._products)  # Отладочный вывод
    print('Prices in repo:', uow.price_repository()._prices)
    print('Users in repo:', uow.user_repository()._users)

    saved_product = uow.product_repository().get('p1')
    saved_price = uow.price_repository().get('pr1')
    saved_user = uow.user_repository().get('u1')
    logger.debug(f'Получены сохраненные объекты: product={saved_product is not None}, price={saved_price is not None}, user={saved_user is not None}')
    logger.debug(f'{saved_product}')
    logger.debug(f'{saved_price}')
    logger.debug(f'{saved_user}')

    assert saved_product is not None
    assert saved_price is not None
    assert saved_user is not None

    print('✅ Цепочка DTO → Entity → UseCase → Service → Repo работает!')