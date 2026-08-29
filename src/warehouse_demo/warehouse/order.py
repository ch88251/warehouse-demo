from dataclasses import dataclass
from datetime import date
from typing import final

from .customer import Customer
from .product import Product


@final
@dataclass
class Order:
    id: int
    customer: "Customer"
    date: date
    quantities: dict["Product", int]
    pending: bool

    def get_total_price(self) -> int:
        return sum(
            product.price * quantity
            for product, quantity in self.quantities.items()
        )

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Order):
            return NotImplemented

        return self.date < other.date