import csv
from dataclasses import asdict
from datetime import datetime

from models.customer_csv_row import CustomerCsvRow


class CustomersCsvGenerator:
    def __init__(self):
        pass

    @staticmethod
    def generate_test_csv():
        with open('data/incoming/customers.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=[
                "customer_id",
                "first_name",
                "last_name",
                "email",
                "country",
                "created_at",
            ])

            writer.writeheader()

            c_csv_row = CustomerCsvRow(
                customer_id="C000001",
                first_name="Anna",
                last_name="Smith",
                email="anna.smith@example.com",
                country="CA",
                created_at=datetime.now())

            writer.writerow(asdict(c_csv_row))

            return [writer, csvfile]




