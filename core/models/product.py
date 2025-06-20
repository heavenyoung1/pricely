from dataclasses import dataclass

@dataclass
class Product:
    id: str
    name: str
    url: str
    marketplace: str # Оптимизировать
    lastPrice: int
    imageUrl: str # Опциональоно


