import csv
import random
from dataclasses import asdict
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

from dictionaries.customer_dictionary import (
    COUNTRY_CODES,
    CUSTOMER_FIELDNAMES,
    FIRST_NAMES,
    LAST_NAMES,
)
from models.customer_csv_row import CustomerCsvRow


class CustomersCsvGenerator:
    OUTPUT_PATH = (
        Path(__file__).resolve().parents[2]
        / "data"
        / "incoming"
        / date.today().isoformat()
        / "customers.csv"
    )

    @classmethod
    def generate_test_csv(cls, customer_count: int) -> Path:
        if isinstance(customer_count, bool) or not isinstance(customer_count, int):
            raise TypeError("customer_count must be an integer")
        if customer_count < 0:
            raise ValueError("customer_count must be non-negative")

        cls.OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

        with cls.OUTPUT_PATH.open("w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=CUSTOMER_FIELDNAMES)
            writer.writeheader()

            for sequence_number in range(1, customer_count + 1):
                customer = cls._generate_customer(sequence_number)
                row = asdict(customer)
                row["created_at"] = customer.created_at.isoformat().replace("+00:00", "Z")
                writer.writerow(row)

        return cls.OUTPUT_PATH

    @classmethod
    def _generate_customer(cls, sequence_number: int) -> CustomerCsvRow:
        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)
        customer_id = f"C{sequence_number:08d}"

        return CustomerCsvRow(
            customer_id=customer_id,
            first_name=first_name,
            last_name=last_name,
            email=(
                f"{first_name}.{last_name}.{customer_id}@example.com".lower()
            ),
            country=random.choice(COUNTRY_CODES),
            created_at=cls._random_utc_datetime(),
        )

    @staticmethod
    def _random_utc_datetime() -> datetime:
        now = datetime.now(timezone.utc)
        earliest = now - timedelta(days=5 * 365)
        available_seconds = int((now - earliest).total_seconds())
        return earliest + timedelta(seconds=random.randint(0, available_seconds))
