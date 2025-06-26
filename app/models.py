from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass
class Entry:
    id: int
    mood: str            # e.g. "happy", "sad", "anxious"
    date: date           # Python date object
    note: Optional[str] = None
