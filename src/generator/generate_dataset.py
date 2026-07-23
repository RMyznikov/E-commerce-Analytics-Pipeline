import argparse
import random
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from src.generator.csv_writer import CsvWriter
from src.generator.customers_generator import CustomersGenerator
from src.generator.order_items_generator import OrderItemsGenerator
from src.generator.orders_generator import OrdersGenerator
from src.generator.payments_generator import PaymentsGenerator
from src.generator.products_generator import ProductsGenerator


@dataclass(frozen=True)
class DatasetConfig:
    customers: int = 100
    products: int = 30
    orders: int = 250
    order_items: int = 750
    seed: int | None = None
    output_dir: Path | None = None


class DatasetGenerator:
    def __init__(self, config: DatasetConfig | None = None) -> None:
        self.config = config or DatasetConfig()
        self._validate_config()
        self._rng = random.Random(self.config.seed)

    def generate(self) -> dict[str, Path]:
        customers = CustomersGenerator(self._rng).generate(self.config.customers)
        products = ProductsGenerator(self._rng).generate(self.config.products)
        orders = OrdersGenerator(customers, self._rng).generate(self.config.orders)
        order_items = OrderItemsGenerator(orders, products, self._rng).generate(
            self.config.order_items
        )
        payments = PaymentsGenerator(
            orders, order_items, products, self._rng
        ).generate()

        output_dir = self.config.output_dir or (
            Path(__file__).resolve().parents[2]
            / "data"
            / "incoming"
            / date.today().isoformat()
        )
        datasets = {
            "customers": customers,
            "products": products,
            "orders": orders,
            "order_items": order_items,
            "payments": payments,
        }

        return {
            name: CsvWriter.write(rows, output_dir / f"{name}.csv")
            for name, rows in datasets.items()
        }

    def _validate_config(self) -> None:
        counts = {
            "customers": self.config.customers,
            "products": self.config.products,
            "orders": self.config.orders,
            "order_items": self.config.order_items,
        }
        for name, value in counts.items():
            if isinstance(value, bool) or not isinstance(value, int):
                raise TypeError(f"{name} must be an integer")
            if value <= 0:
                raise ValueError(f"{name} must be greater than zero")
        if self.config.order_items < self.config.orders:
            raise ValueError("order_items must be at least equal to orders")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate an e-commerce CSV dataset")
    parser.add_argument("--customers", type=int, default=100)
    parser.add_argument("--products", type=int, default=30)
    parser.add_argument("--orders", type=int, default=250)
    parser.add_argument("--order-items", type=int, default=750)
    parser.add_argument("--seed", type=int)
    parser.add_argument("--output-dir", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    paths = DatasetGenerator(
        DatasetConfig(
            customers=args.customers,
            products=args.products,
            orders=args.orders,
            order_items=args.order_items,
            seed=args.seed,
            output_dir=args.output_dir,
        )
    ).generate()
    for name, path in paths.items():
        print(f"{name}: {path}")


if __name__ == "__main__":
    main()
