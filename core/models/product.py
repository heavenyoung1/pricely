from dataclasses import dataclass
from typing import Dict

@dataclass
class Product:
    id: str
    name: str
    url: str
    marketplace: str # Оптимизировать
    last_price: int
    image_url: str # Опциональоно

    def update_price(self, new_price: int) -> Dict:
        changed: bool = self.last_price != new_price
        result = {
            'name': self.name,
            'changed': changed,
            'last_price': self.last_price,
            'new_price': new_price,
        }

        if changed:
            self.last_price = new_price
            return result
        return result

