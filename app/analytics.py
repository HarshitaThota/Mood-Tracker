# Role: encapsulate all reporting logic so it’s easy to test and swap in/out.
from collections import Counter
from datetime import date, timedelta
from typing import List, Dict, Optional

from .models import Entry


# ---------- helpers ----------
def _sorted_by_date(entries: List[Entry]) -> List[Entry]:
    return sorted(entries, key=lambda e: e.date)


# ---------- public API ----------
def filter_by_date(
    entries: List[Entry],
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
) -> List[Entry]:
    """Return entries where date_from ≤ date ≤ date_to (both inclusive)."""
    out = entries
    if date_from:
        out = [e for e in out if e.date >= date_from]
    if date_to:
        out = [e for e in out if e.date <= date_to]
    return _sorted_by_date(out)


def distribution(entries: List[Entry]) -> Dict[str, int]:
    """Count occurrences of each mood"""
    return Counter(e.mood for e in entries)


def longest_streak(entries: List[Entry]) -> Dict[str, int]:
    """
    Returns a mapping {mood: longest_consecutive_days}
    Example: {'happy': 3, 'sad': 2}
    """
    # prep: {date: mood}
    by_day = {e.date: e.mood for e in entries}
    moods = set(by_day.values())
    streaks = {m: 0 for m in moods}

    for mood in moods:
        current = 0
        max_streak = 0
        for entry in _sorted_by_date(entries):
            if entry.mood == mood:
                # Check previous day continuity
                prev = entry.date - timedelta(days=1)
                if by_day.get(prev) == mood:
                    current += 1
                else:
                    current = 1
                max_streak = max(max_streak, current)
        streaks[mood] = max_streak
    return streaks
