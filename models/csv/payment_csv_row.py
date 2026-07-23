from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass(frozen=True)
class PaymentCsvRow:
    payment_id: str
    order_id: str
    payment_method: str
    amount: Decimal
    payment_status: str
    paid_at: datetime
