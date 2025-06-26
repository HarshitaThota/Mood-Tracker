import json
from pathlib import Path
import pytest
from datetime import date

from app.repository import load_entries, save_entries, STORAGE
from app.models import Entry

def test_load_nonexistent(tmp_path, monkeypatch):
    fake = tmp_path / "nope.json"
    # ensure it really doesn't exist
    if fake.exists():
        fake.unlink()
    entries = load_entries(path=fake)
    assert entries == []

def test_save_and_load_roundtrip(tmp_path):
    file = tmp_path / "entries.json"

    # prepare some Entries
    e1 = Entry(id=1, mood="happy", date=date(2024,6,1), note="yay")
    e2 = Entry(id=2, mood="sad",   date=date(2024,6,2), note=None)
    save_entries([e1, e2], path=file)

    # raw JSON shape
    raw = json.loads(file.read_text())
    assert raw == [
        {"id": 1, "mood": "happy", "date": "2024-06-01", "note": "yay"},
        {"id": 2, "mood": "sad",   "date": "2024-06-02", "note": None},
    ]

    # load back as Entry objects
    loaded = load_entries(path=file)
    assert [ (e.id,e.mood,e.date,e.note) for e in loaded ] == [
        (1, "happy", date(2024,6,1), "yay"),
        (2, "sad",   date(2024,6,2), None),
    ]

def test_atomic_write(tmp_path):
    file = tmp_path / "entries.json"
    # Pre-create a bad file so that .tmp → replace flows
    file.write_text("BROKEN JSON")
    # Now save new valid data
    entry = Entry(id=42, mood="meh", date=date(2024,1,1), note="")
    save_entries([entry], path=file)

    # Ensure we never saw leftover “BROKEN JSON”
    data = json.loads(file.read_text())
    assert data[0]["id"] == 42
