import csv
import tempfile
import unittest
from dataclasses import is_dataclass
from pathlib import Path

from models.csv.customer_csv_row import CustomerCsvRow
from models.csv.order_csv_row import OrderCsvRow
from models.csv.order_item_csv_row import OrderItemCsvRow
from models.csv.payment_csv_row import PaymentCsvRow
from models.csv.product_csv_row import ProductCsvRow
from src.generator.generate_dataset import DatasetConfig, DatasetGenerator


class DatasetGeneratorTest(unittest.TestCase):
    def test_models_are_dataclasses(self) -> None:
        for model in (
            CustomerCsvRow,
            ProductCsvRow,
            PaymentCsvRow,
            OrderCsvRow,
            OrderItemCsvRow,
        ):
            self.assertTrue(is_dataclass(model))

    def test_generates_expected_rows_and_valid_foreign_keys(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            counts = {
                "customers": 7,
                "products": 5,
                "orders": 12,
                "order_items": 30,
            }
            paths = DatasetGenerator(
                DatasetConfig(
                    **counts,
                    seed=42,
                    output_dir=Path(temporary_directory),
                )
            ).generate()
            rows = {name: self._read_csv(path) for name, path in paths.items()}

            for name, count in counts.items():
                self.assertEqual(count, len(rows[name]))
            self.assertEqual(counts["orders"], len(rows["payments"]))
            self.assertEqual(
                ["order_id", "ordered_at", "status", "customer_id"],
                list(rows["orders"][0]),
            )
            self.assertEqual(
                [
                    "payment_id",
                    "order_id",
                    "payment_method",
                    "amount",
                    "payment_status",
                    "paid_at",
                ],
                list(rows["payments"][0]),
            )

            customer_ids = {row["customer_id"] for row in rows["customers"]}
            product_ids = {row["product_id"] for row in rows["products"]}
            order_ids = {row["order_id"] for row in rows["orders"]}

            self.assertLessEqual(
                {row["customer_id"] for row in rows["orders"]}, customer_ids
            )
            self.assertLessEqual(
                {row["product_id"] for row in rows["order_items"]}, product_ids
            )
            self.assertEqual(
                {row["order_id"] for row in rows["order_items"]}, order_ids
            )
            payment_order_ids = [
                row["order_id"] for row in rows["payments"]
            ]
            self.assertEqual(set(payment_order_ids), order_ids)
            self.assertEqual(len(payment_order_ids), len(set(payment_order_ids)))

            prices = {
                row["product_id"]: float(row["unit_price"])
                for row in rows["products"]
            }
            expected_totals = {order_id: 0.0 for order_id in order_ids}
            for item in rows["order_items"]:
                expected_totals[item["order_id"]] += (
                    prices[item["product_id"]] * int(item["quantity"])
                )
            for payment in rows["payments"]:
                self.assertAlmostEqual(
                    float(payment["amount"]),
                    expected_totals[payment["order_id"]],
                    places=2,
                )

    def test_rejects_zero_sized_dependency_dataset(self) -> None:
        with self.assertRaisesRegex(ValueError, "customers"):
            DatasetGenerator(DatasetConfig(customers=0))

    def test_rejects_fewer_items_than_orders(self) -> None:
        with self.assertRaisesRegex(ValueError, "order_items"):
            DatasetGenerator(DatasetConfig(orders=10, order_items=9))

    @staticmethod
    def _read_csv(path: Path) -> list[dict[str, str]]:
        with path.open(encoding="utf-8", newline="") as csv_file:
            return list(csv.DictReader(csv_file))


if __name__ == "__main__":
    unittest.main()
