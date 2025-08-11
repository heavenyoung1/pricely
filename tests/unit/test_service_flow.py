from src.interfaces.dto.product_dto import ProductCreateDTO, PriceCreateDTO, UserCreateDTO
from src.application.services.product_service import ProductService

from src.interfaces.dto.dto_to_entity import (
    product_dto_to_entity, 
    price_dto_to_entity, 
    user_dto_to_entity
    )

from tests.unit.fake_uow import FakeUnitOfWork

def test_full_flow():
    uow_factory = lambda: FakeUnitOfWork()
    service = ProductService(uow_factory)

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

    product_entity = product_dto_to_entity(product_dto)
    price_entity = price_dto_to_entity(price_dto)
    user_entity = user_dto_to_entity(user_dto)

    # 2. ENTITY → UseCase → Service → Repo
    service.create_product_with_price(product_entity, price_entity, user_entity)

    uow = uow_factory()
    saved_product = uow.product_repository.get('p1')
    saved_price = uow.price_repository.get('pr1')
    saved_user = uow.user_repository.get('u1')

    assert saved_product is not None
    assert saved_price is not None
    assert 'p1' is not None

    print("✅ Цепочка DTO → Entity → UseCase → Service → Repo работает!")