from dataclasses import dataclass

@dataclass(frozen=True)
class CarSale:
    # Keeping it Frozen so we dont accidently modify the data 
    id: int
    price: float
    brand: str
    model: str
    year: int
    title_status: str
    mileage: float
    color: str

    @property
    def full_name(self) -> str:
        # standardizing brand+model key for aggregation
        return f"{self.brand} {self.model}"