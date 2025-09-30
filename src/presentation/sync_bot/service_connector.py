from src.infrastructure.services.product_service import ProductService
from src.core import SQLAlchemyUnitOfWork

service = ProductService(uow_factory=SQLAlchemyUnitOfWork)