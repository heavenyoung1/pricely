from typing import Optional
from domain.entities.user_products import UserProductsData
from domain.entities.product_fields import ProductFields

class ProductParser():
    def __init__(
            self,
            data: UserProductsData,
            fields: ProductFields,
            ) -> None:

        self.fields = fields
        self.data = data
