import csv
from dataclasses import is_dataclass
from pathlib import Path

import pytest

from models.csv.customer_csv_row import CustomerCsvRow
from models.csv.order_csv_row import OrderCsvRow
from models.csv.order_item_csv_row import OrderItemCsvRow
from models.csv.payment_csv_row import PaymentCsvRow
from models.csv.product_csv_row import ProductCsvRow
from src.generator.generate_dataset import DatasetConfig, DatasetGenerator


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as csv_file:
        return list(csv.DictReader(csv_file))


def test_models_are_dataclasses() -> None:
    models = (
        CustomerCsvRow,
        ProductCsvRow,
        PaymentCsvRow,
        OrderCsvRow,
        OrderItemCsvRow,
    )

    assert all(is_dataclass(model) for model in models)


def test_generates_expected_rows_and_valid_foreign_keys(tmp_path: Path) -> None:
    counts = {
        "customers": 7,
        "products": 5,
        "orders": 12,
        "order_items": 30,
    }
    paths = DatasetGenerator(
        DatasetConfig(**counts, seed=42, output_dir=tmp_path)
    ).generate()
    rows = {name: read_csv(path) for name, path in paths.items()}

    for name, count in counts.items():
        assert len(rows[name]) == count
    assert len(rows["payments"]) == counts["orders"]
    assert list(rows["orders"][0]) == [
        "order_id",
        "ordered_at",
        "status",
        "customer_id",
    ]
    assert list(rows["payments"][0]) == [
        "payment_id",
        "order_id",
        "payment_method",
        "amount",
        "payment_status",
        "paid_at",
    ]

    customer_ids = {row["customer_id"] for row in rows["customers"]}
    product_ids = {row["product_id"] for row in rows["products"]}
    order_ids = {row["order_id"] for row in rows["orders"]}

    assert {row["customer_id"] for row in rows["orders"]} <= customer_ids
    assert {row["product_id"] for row in rows["order_items"]} <= product_ids
    assert {row["order_id"] for row in rows["order_items"]} == order_ids

    payment_order_ids = [row["order_id"] for row in rows["payments"]]
    assert set(payment_order_ids) == order_ids
    assert len(payment_order_ids) == len(set(payment_order_ids))

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
        assert float(payment["amount"]) == pytest.approx(
            expected_totals[payment["order_id"]], abs=0.01
        )


def test_rejects_zero_sized_dependency_dataset() -> None:
    with pytest.raises(ValueError, match="customers"):
        DatasetGenerator(DatasetConfig(customers=0))


def test_rejects_fewer_items_than_orders() -> None:
    with pytest.raises(ValueError, match="order_items"):
        DatasetGenerator(DatasetConfig(orders=10, order_items=9))
