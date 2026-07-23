import random

from models.csv.order_csv_row import OrderCsvRow
from models.csv.order_item_csv_row import OrderItemCsvRow
from models.csv.product_csv_row import ProductCsvRow


class OrderItemsGenerator:
    def __init__(
        self,
        orders: list[OrderCsvRow],
        products: list[ProductCsvRow],
        rng: random.Random | None = None,
    ) -> None:
        if not orders:
            raise ValueError("orders must not be empty")
        if not products:
            raise ValueError("products must not be empty")
        self._orders = orders
        self._products = products
        self._rng = rng or random.Random()

    def generate(self, count: int) -> list[OrderItemCsvRow]:
        self._validate_count(count)
        if count < len(self._orders):
            raise ValueError("count must be at least the number of orders")

        guaranteed_orders = list(self._orders)
        self._rng.shuffle(guaranteed_orders)

        return [
            OrderItemCsvRow(
                order_item_id=f"OI{number:010d}",
                quantity=self._rng.randint(1, 5),
                product_id=self._rng.choice(self._products).product_id,
                order_id=(
                    guaranteed_orders[number - 1]
                    if number <= len(guaranteed_orders)
                    else self._rng.choice(self._orders)
                ).order_id,
            )
            for number in range(1, count + 1)
        ]

    @staticmethod
    def _validate_count(count: int) -> None:
        if isinstance(count, bool) or not isinstance(count, int):
            raise TypeError("count must be an integer")
        if count < 0:
            raise ValueError("count must be non-negative")
