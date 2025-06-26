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
def test_filter_by_date_only_from():
    out = filter_by_date(SAMPLE, date(2024,6,22), None)
    assert [e.id for e in out] == [3,4,5]

def test_filter_by_date_only_to():
    out = filter_by_date(SAMPLE, None, date(2024,6,21))
    assert [e.id for e in out] == [1,2]

def test_filter_by_date_no_bounds_and_unsorted():
    # reverse the list to force sorting
    out = filter_by_date(list(reversed(SAMPLE)))
    assert [e.id for e in out] == [1,2,3,4,5]

def test_distribution_empty():
    assert distribution([]) == {}

def test_longest_streak_empty():
    assert longest_streak([]) == {}

def test_longest_streak_unsorted():
    # even if input is jumbled, streak logic should pick up the 3-day happy run
    jumbled = [SAMPLE[2], SAMPLE[0], SAMPLE[1]]
    assert longest_streak(jumbled) == {"happy": 3}

def test_longest_streak_multiple_bursts():
    # mood 'x' has two separate 2-day streaks → max should be 2
    ent = [
      _e(1, "x", "2024-06-01"),
      _e(2, "x", "2024-06-02"),
      _e(3, "x", "2024-06-07"),
      _e(4, "x", "2024-06-08"),
    ]
    assert longest_streak(ent) == {"x": 2}