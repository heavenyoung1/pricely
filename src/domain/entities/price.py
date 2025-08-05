from pydantic.dataclasses import dataclass

# Strict Mode - Строгий режим, запрещающий конвертацию типов 
@dataclass(strict=True)
class Price:
    with_card: int
    without_card: int
    previous_with_card: int
    previous_without_card: int
    default: int