# Mood Tracker

A tiny CLI (with optional Flask UI) that lets you log daily moods, then view
distributions, streaks, and trends.  
*Stack choices: Python 3.11 • Click CLI • JSON (or SQLite) persistence.*

## Quick start
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
mood add --type happy --date 2024-06-26 --note "Lunch with friends"
mood report distribution

app/              # source code package
tests/            # pytest unit tests
sample_data/      # seed JSON for demo
