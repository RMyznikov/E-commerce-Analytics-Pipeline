from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class ProductCsvRow:
    product_id: str
    name: str
    category: str
    unit_price: Decimal
