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
    """Return entries where date_from ≤ date ≤ date_to (inclusive), sorted by date."""
    out = entries
    if date_from:
        out = [e for e in out if e.date >= date_from]
    if date_to:
        out = [e for e in out if e.date <= date_to]
    return _sorted_by_date(out)


def distribution(entries: List[Entry]) -> Dict[str, int]:
    """Count occurrences of each mood."""
    return Counter(e.mood for e in entries)


def longest_streak(entries: List[Entry]) -> Dict[str, int]:
    """
    Returns a mapping {mood: longest_consecutive_days}.
    If multiple entries exist on the same date, the latest entry is used.
    """
    # Build a mapping of date → last mood on that date
    by_day: Dict[date, str] = {}
    for e in _sorted_by_date(entries):
        by_day[e.date] = e.mood  # later entries overwrite earlier ones

    moods = set(by_day.values())
    streaks = {m: 0 for m in moods}

    # Iterate through each mood and compute its longest run
    all_dates = sorted(by_day)
    for mood in moods:
        current = 0
        max_streak = 0
        for today in all_dates:
            if by_day[today] == mood:
                yesterday = today - timedelta(days=1)
                if by_day.get(yesterday) == mood:
                    current += 1
                else:
                    current = 1
                max_streak = max(max_streak, current)
        streaks[mood] = max_streak

    return streaks
