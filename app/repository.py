# Role: keep all I/O and data-format concerns here, isolated from business logic
import json
from pathlib import Path
from datetime import datetime
from typing import List

from .models import Entry

STORAGE = Path("sample_data/entries.json")

def load_entries(path: Path = STORAGE) -> List[Entry]:
    if not path.exists():
        return []
    raw = json.loads(path.read_text())
    return [
        Entry(
            id=r["id"],
            mood=r["mood"],
            date=datetime.fromisoformat(r["date"]).date(),
            note=r.get("note")
        ) for r in raw
    ]

def save_entries(entries: List[Entry], path: Path = STORAGE) -> None:
    tmp = path.with_suffix(".tmp")
    payload = [e.__dict__.copy() for e in entries]
    for p in payload:
        p["date"] = p["date"].isoformat()
    tmp.write_text(json.dumps(payload, indent=2))
    tmp.replace(path)



# Persistence refers to the ability of data to outlive the process that created it.
# It means that when a program terminates, the data it was working with can be saved
# and later retrieved by another process or the same process when it's restarted.
# Essentially, persistence allows you to store and access data across multiple program executions.