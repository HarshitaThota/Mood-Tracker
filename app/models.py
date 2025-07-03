from dataclasses import dataclass
from datetime import date # Python’s standard datetime library
from typing import Optional 

@dataclass 
class Entry:
    id: int    # an auto-incrementing unique key so we can easily reference individual records in the future
    mood: str            # free form label, e.g. "happy", "sad", "anxious"
    date: date           # stored internally as a date object to guarantee valid dates making range filtering trivial
    note: Optional[str] = None  # optional note, can be None if not provided
