import csv
from typing import Iterator
from src.models import CarSale

def car_sales_stream(filepath: str) -> Iterator[CarSale]:

    #  Lazy generator: Reads CSV one line at a time.
    try:
        with open(filepath, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    # Convert raw CSV strings to proper types
                    yield CarSale(
                        id=int(row['id']),
                        price=float(row['price']),
                        brand=row['brand'],
                        model=row['model'],
                        year=int(row['year']),
                        title_status=row['title_status'],
                        mileage=float(row['mileage']),
                        color=row['color']
                    )
                except (ValueError, KeyError):
                    # Skip this specific row to keep the stream alive.:
                    continue
    except FileNotFoundError:
        print(f"Error: File {filepath} not found.")
        return