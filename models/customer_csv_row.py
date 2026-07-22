from dataclasses import dataclass
from datetime import datetime


@dataclass
class CustomerCsvRow:
    customer_id: str
    first_name: str
    last_name: str
    email: str
    country: str
    created_at: datetime
