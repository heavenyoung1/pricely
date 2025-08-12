from src.domain.entities import Product, Price, User
from src.interfaces.dto.product_dto import ProductCreateDTO, PriceCreateDTO, UserCreateDTO

# Это адаптер между входными DTO и доменом.

def product_dto_to_entity(dto: PriceCreateDTO) -> Product:
    return Product(
        id=dto.id,
        user_id=dto.user_id,
        price_id='',  # пока пусто, заполнит UseCase
        name=dto.name,
        link=str(dto.link),
        image_url=str(dto.image_url),
        rating=dto.rating,
        categories=dto.categories
    )

def price_dto_to_entity(dto: PriceCreateDTO) -> Price:
    return Price(
        id=dto.id,
        product_id=dto.product_id,
        with_card=dto.with_card,
        without_card=dto.without_card,
        previous_with_card=dto.previous_with_card,
        previous_without_card=dto.previous_without_card,
        default=dto.default,
        claim=dto.claim
    )

def user_dto_to_entity(dto: UserCreateDTO) -> User:
    return User(
       id=dto.id,
       username=dto.username,
       chat_id=dto.chat_id,
       products=dto.products, 
    )