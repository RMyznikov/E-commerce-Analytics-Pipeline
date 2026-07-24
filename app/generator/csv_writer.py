import csv
from dataclasses import asdict, fields, is_dataclass
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path
from typing import Any


class CsvWriter:
    @classmethod
    def write(cls, rows: list[Any], output_path: Path) -> Path:
        if not rows:
            raise ValueError("rows must not be empty")
        if not is_dataclass(rows[0]) or isinstance(rows[0], type):
            raise TypeError("rows must contain dataclass instances")

        row_type = type(rows[0])
        if any(type(row) is not row_type for row in rows):
            raise TypeError("all rows must have the same dataclass type")

        output_path.parent.mkdir(parents=True, exist_ok=True)
        fieldnames = [field.name for field in fields(rows[0])]

        with output_path.open("w", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for row in rows:
                writer.writerow(
                    {
                        key: cls._serialize(value)
                        for key, value in asdict(row).items()
                    }
                )

        return output_path

    @staticmethod
    def _serialize(value: Any) -> Any:
        if isinstance(value, datetime):
            return value.isoformat().replace("+00:00", "Z")
        if isinstance(value, date):
            return value.isoformat()
        if isinstance(value, Decimal):
            return format(value, "f")
        return value
