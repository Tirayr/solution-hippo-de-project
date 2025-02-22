from dataclasses import dataclass
from datetime import datetime

@dataclass
class Revert:
    id: str
    claim_id: str
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
            claim_id=data['claim_id'],
            timestamp=timestamp
        )