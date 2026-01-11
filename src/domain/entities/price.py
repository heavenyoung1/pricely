from dataclasses import dataclass


@dataclass
class Price:
    id: int
    product_id: int
    with_card: int
    without_card: int
    previous_with_card: int
    previous_without_card: int
