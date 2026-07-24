from dataclasses import dataclass


@dataclass(frozen=True)
class OrderItemCsvRow:
    order_item_id: str
    quantity: int
    product_id: str
    order_id: str
