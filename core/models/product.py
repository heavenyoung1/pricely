from dataclasses import dataclass

@dataclass
class Product:
    id: str
    name: str
    url: str
    marketplace: str # Оптимизировать
    last_price: int
    image_url: str # Опциональоно


