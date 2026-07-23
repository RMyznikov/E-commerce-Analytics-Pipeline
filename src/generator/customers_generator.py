import random
from datetime import datetime, timedelta, timezone

from models.csv.customer_csv_row import CustomerCsvRow


class CustomersGenerator:
    _FIRST_NAMES = (
        "Anna", "Emma", "Olivia", "Sophia", "Mia", "Liam", "Noah", "Lucas",
        "James", "Daniel", "Maria", "Sofia", "Ivan", "Oleh", "Iryna", "Marta",
    )
    _LAST_NAMES = (
        "Smith", "Johnson", "Brown", "Wilson", "Taylor", "Anderson", "Martin",
        "Clark", "Walker", "Young", "Koval", "Melnyk", "Bondarenko",
        "Shevchenko",
    )
    _COUNTRY_CODES = (
        "AU", "BR", "CA", "DE", "ES", "FR", "GB", "IN", "IT", "JP", "MX",
        "NL", "PL", "SE", "UA", "US",
    )

    def __init__(self, rng: random.Random | None = None) -> None:
        self._rng = rng or random.Random()

    def generate(self, count: int) -> list[CustomerCsvRow]:
        self._validate_count(count)
        return [self._generate_customer(number) for number in range(1, count + 1)]

    def _generate_customer(self, number: int) -> CustomerCsvRow:
        first_name = self._rng.choice(self._FIRST_NAMES)
        last_name = self._rng.choice(self._LAST_NAMES)
        customer_id = f"C{number:08d}"

        return CustomerCsvRow(
            customer_id=customer_id,
            first_name=first_name,
            last_name=last_name,
            email=f"{first_name}.{last_name}.{customer_id}@example.com".lower(),
            country=self._rng.choice(self._COUNTRY_CODES),
            created_at=self._random_created_at(),
        )

    def _random_created_at(self) -> datetime:
        now = datetime.now(timezone.utc)
        earliest = now - timedelta(days=5 * 365)
        seconds = int((now - earliest).total_seconds())
        return earliest + timedelta(seconds=self._rng.randint(0, seconds))

    @staticmethod
    def _validate_count(count: int) -> None:
        if isinstance(count, bool) or not isinstance(count, int):
            raise TypeError("count must be an integer")
        if count < 0:
            raise ValueError("count must be non-negative")
