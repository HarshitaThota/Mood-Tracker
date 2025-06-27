# app/service.py
from datetime import date
from .models import Entry
from .repository import load_entries, save_entries
from .analytics import filter_by_date, distribution, longest_streak

def add_entry(mood: str, d: str, note: str = None) -> Entry:
    entries = load_entries()
    new_id = max((e.id for e in entries), default=0) + 1
    entry = Entry(id=new_id,
                  mood=mood,
                  date=date.fromisoformat(d),
                  note=note)
    entries.append(entry)
    save_entries(entries)
    return entry

def list_entries(date_from: str = None, date_to: str = None):
    entries = load_entries()
    df = date.fromisoformat(date_from) if date_from else None
    dt = date.fromisoformat(date_to)   if date_to   else None
    return filter_by_date(entries, df, dt)

def get_distribution(date_from: str = None, date_to: str = None):
    entries = list_entries(date_from, date_to)
    return distribution(entries)

def get_streak(date_from: str = None, date_to: str = None):
    entries = list_entries(date_from, date_to)
    return longest_streak(entries)
