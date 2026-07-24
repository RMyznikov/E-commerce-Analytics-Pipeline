import random
from decimal import Decimal

from app.models.csv.product_csv_row import ProductCsvRow


class ProductsGenerator:
    _PRODUCTS = (
        ("Wireless Mouse", "Electronics"),
        ("Mechanical Keyboard", "Electronics"),
        ("Cotton T-Shirt", "Clothing"),
        ("Running Shoes", "Clothing"),
        ("Coffee Maker", "Home"),
        ("Desk Lamp", "Home"),
        ("Python Handbook", "Books"),
        ("Travel Backpack", "Accessories"),
    )

    def __init__(self, rng: random.Random | None = None) -> None:
        self._rng = rng or random.Random()

    def generate(self, count: int) -> list[ProductCsvRow]:
        self._validate_count(count)
        products = []

        for number in range(1, count + 1):
            base_name, category = self._rng.choice(self._PRODUCTS)
            price = Decimal(self._rng.randint(500, 50_000)) / Decimal("100")
            products.append(
                ProductCsvRow(
                    product_id=f"P{number:08d}",
                    name=f"{base_name} {number}",
                    category=category,
                    unit_price=price,
                )
            )

        return products

    @staticmethod
    def _validate_count(count: int) -> None:
        if isinstance(count, bool) or not isinstance(count, int):
            raise TypeError("count must be an integer")
        if count < 0:
            raise ValueError("count must be non-negative")
