from datetime import date

from app.models import Entry
from app.analytics import filter_by_date, distribution, longest_streak


def _e(id, mood, d):  # tiny helper
    return Entry(id=id, mood=mood, date=date.fromisoformat(d))


SAMPLE = [
    _e(1, "happy", "2024-06-20"),
    _e(2, "happy", "2024-06-21"),
    _e(3, "happy", "2024-06-22"),
    _e(4, "sad", "2024-06-24"),
    _e(5, "sad", "2024-06-26"),
]

def test_filter_by_date():
    out = filter_by_date(SAMPLE, date.fromisoformat("2024-06-21"), date.fromisoformat("2024-06-24"))
    assert [e.id for e in out] == [2, 3, 4]

def test_distribution():
    assert distribution(SAMPLE) == {"happy": 3, "sad": 2}

def test_longest_streak():
    assert longest_streak(SAMPLE) == {"happy": 3, "sad": 1}
