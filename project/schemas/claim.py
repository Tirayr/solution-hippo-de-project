from dataclasses import dataclass
from datetime import datetime

@dataclass
class Claim:
    id: str
    npi: str
    ndc: str
    price: float
    quantity: int
    timestamp: datetime

    @classmethod
    def from_dict(cls, data: dict):
        try:
            # Assuming timestamp is in ISO format
            timestamp = datetime.fromisoformat(data['timestamp'])
        except ValueError as e:
            raise ValueError(f"Invalid timestamp format: {e}")

        return cls(
            id=data['id'],
            npi=data['npi'],
            ndc=data['ndc'],
            price=float(data['price']),
            quantity=int(data['quantity']),
            timestamp=timestamp
        )
