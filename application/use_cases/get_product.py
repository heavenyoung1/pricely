from typing import Optional

from infrastructure.database.unit_of_work import UnitOfWorkFactory
from domain.entities.product import FullProduct
from domain.exceptions import ProductNotFoundError


class GetProductUseCase:
    def __init__(self, uow_factory: UnitOfWorkFactory):
        self.uow_factory = uow_factory

    async def execute(self, product_id: int) -> Optional[FullProduct]:
        async with self.uow_factory.create() as uow:
            product = await uow.product_repo.get(product_id)
            if not product:
                raise ProductNotFoundError(product_id)

            price = await uow.price_repo.get_actual(product_id)

            return FullProduct(
                id=product.id,
                article=product.article,
                name=product.name,
                link=product.link,
                price_with_card=price.with_card,
                price_without_card=price.without_card,
                price_previous_with_card=price.previous_with_card,
                price_previous_without_card=price.previous_without_card,
                change=product.change,
            )
