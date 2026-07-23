import random
from datetime import datetime, timedelta
from decimal import Decimal

from models.csv.order_csv_row import OrderCsvRow
from models.csv.order_item_csv_row import OrderItemCsvRow
from models.csv.payment_csv_row import PaymentCsvRow
from models.csv.product_csv_row import ProductCsvRow


class PaymentsGenerator:
    _PAYMENT_METHODS = (
        "card",
        "digital_wallet",
        "bank_transfer",
    )

    def __init__(
        self,
        orders: list[OrderCsvRow],
        order_items: list[OrderItemCsvRow],
        products: list[ProductCsvRow],
        rng: random.Random | None = None,
    ) -> None:
        if not orders:
            raise ValueError("orders must not be empty")
        if not order_items:
            raise ValueError("order_items must not be empty")
        if not products:
            raise ValueError("products must not be empty")
        self._orders = orders
        self._order_items = order_items
        self._products = products
        self._rng = rng or random.Random()

    def generate(self) -> list[PaymentCsvRow]:
        prices = {product.product_id: product.unit_price for product in self._products}
        totals = {order.order_id: Decimal("0") for order in self._orders}
        for item in self._order_items:
            totals[item.order_id] += prices[item.product_id] * item.quantity

        return [
            PaymentCsvRow(
                payment_id=f"PAY{number:04d}",
                order_id=order.order_id,
                payment_method=self._rng.choice(self._PAYMENT_METHODS),
                amount=totals[order.order_id],
                payment_status=(
                    "refunded" if order.status == "cancelled" else "completed"
                ),
                paid_at=order.ordered_at + timedelta(
                    seconds=self._rng.randint(1, 3600)
                ),
            )
            for number, order in enumerate(self._orders, start=1)
        ]
