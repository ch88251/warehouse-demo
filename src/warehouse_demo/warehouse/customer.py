from dataclasses import dataclass
from typing import final


@final
@dataclass
class Customer:
    customer_id: str
    name: str