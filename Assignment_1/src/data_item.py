from typing import Optional, Any

class DataItem:
    """
    A wrapper class for data transferred between Producer and Consumer.
    
    Attributes:
        payload (Any): The actual data. If None, represents a Poison Pill.
    """
    def __init__(self, payload: Optional[Any]):
        self.payload = payload

    def is_poison_pill(self) -> bool:
        """Checks if this item is the signal to stop processing."""
        return self.payload is None

    def __repr__(self) -> str:
        return f"DataItem(payload={self.payload})"