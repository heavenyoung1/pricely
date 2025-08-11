from src.interfaces.dto.product_dto import ProductCreateDTO, PriceCreateDTO, UserCreateDTO
from src.interfaces.dto.mappers import product_dto_to_entity, price_dto_to_entity, user_dto_to_entity
from src.application.services.product_service import ProductService
from tests.fake_uow import FakeUnitOfWork

