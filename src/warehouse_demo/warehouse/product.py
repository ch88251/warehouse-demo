from dataclasses import dataclass
from typing import final


@final
@dataclass
class Product:
    product_id: str
    name: str
    price: float

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Product):
            return NotImplemented

        return self.price < other.price