from aiogram import Router

from .start import router as start_router
from .product import router as product_router


def setup_routers() -> Router:
    '''Собирает все роутеры в один'''
    router = Router()
    router.include_router(start_router)
    router.include_router(product_router)
    return router
