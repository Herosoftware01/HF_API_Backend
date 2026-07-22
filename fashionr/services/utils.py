from datetime import datetime
import re
from decimal import Decimal

def parse_date(value):
    if not value:
        return None

    formats = [
        "%d-%m-%Y",
        "%Y-%m-%d",
        "%m/%d/%Y",
    ]

    for fmt in formats:
        try:
            return datetime.strptime(value, fmt).date()
        except ValueError:
            continue

    return None

def parse_time(value):
    if not value:
        return None

    formats = [
        "%H:%M:%S",
        "%H:%M",
        "%I:%M:%S %p",
        "%I:%M %p",
        "%m/%d/%Y %I:%M:%S %p",
        "%m/%d/%Y %I:%M %p",
    ]

    for fmt in formats:
        try:
            return datetime.strptime(value, fmt).time()
        except ValueError:
            continue

    return None

def safe_decimal(value):
    if value is None:
        return None

    value = str(value).strip()
    match = re.search(r'-?\d+(\.\d+)?', value)
    if match:
        return Decimal(match.group())

    return None

