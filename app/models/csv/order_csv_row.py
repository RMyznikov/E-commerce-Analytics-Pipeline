from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class OrderCsvRow:
    order_id: str
    ordered_at: datetime
    status: str
    customer_id: str
