import random
from datetime import datetime, timedelta, timezone

from app.models.csv.customer_csv_row import CustomerCsvRow
from app.models.csv.order_csv_row import OrderCsvRow


class OrdersGenerator:
    _STATUSES = ("completed", "completed", "completed", "shipped", "cancelled")

    def __init__(
        self,
        customers: list[CustomerCsvRow],
        rng: random.Random | None = None,
    ) -> None:
        if not customers:
            raise ValueError("customers must not be empty")
        self._customers = customers
        self._rng = rng or random.Random()

    def generate(self, count: int) -> list[OrderCsvRow]:
        self._validate_count(count)
        now = datetime.now(timezone.utc)
        orders = []

        for number in range(1, count + 1):
            customer = self._rng.choice(self._customers)
            available_seconds = max(
                0, int((now - customer.created_at).total_seconds())
            )
            ordered_at = customer.created_at
            if available_seconds:
                ordered_at += timedelta(
                    seconds=self._rng.randint(0, available_seconds)
                )

            orders.append(
                OrderCsvRow(
                    order_id=f"O{number:09d}",
                    ordered_at=ordered_at,
                    status=self._rng.choice(self._STATUSES),
                    customer_id=customer.customer_id,
                )
            )

        return orders

    @staticmethod
    def _validate_count(count: int) -> None:
        if isinstance(count, bool) or not isinstance(count, int):
            raise TypeError("count must be an integer")
        if count < 0:
            raise ValueError("count must be non-negative")
