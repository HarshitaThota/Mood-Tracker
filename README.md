# Daily Mood Tracker

A small, fully-tested Python app for logging and analyzing your daily moods via:

- **CLI** (Click-based)  
- **(Optional)** Flask-powered web UI  
- **Storage**: JSON file by default (SQLite stubbed)  

---

## 📋 Table of Contents

1. [Features](#features)  
2. [Getting Started](#getting-started)  
3. [Usage](#usage)  
4. [Project Structure](#project-structure)  
5. [Architecture](#architecture)  
6. [Running Tests](#running-tests)  
7. [Roadmap & Next Steps](#roadmap--next-steps)  
8. [Contact](#contact)  

---

## 🚀 Features

- **Add** a mood entry: date, mood type (happy, sad, anxious,…), optional note.  
- **List** entries by date range.  
- **Reports**:  
  - **Distribution**: count of each mood  
  - **Streak**: your longest run of the same mood  
  - **Trend**: sliding-window mood summary (e.g. 7-day)  
- **Storage**: JSON (no external DB) or SQLite (optional).  
- **Extensible**: easily swap-out storage, add a Flask UI, or package as a CLI tool.

---

## 🛠️ Getting Started


1. Clone & enter
git clone https://github.com/HarshitaThota/Mood-Tracker.git
cd Mood-Tracker

2. Create & activate venv
python3 -m venv .venv
source .venv/bin/activate      # macOS/Linux
.venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r requirements.txt



# Add a new entry
mood add --mood happy --date 2024-06-26 --note "Lunch with friends"

# List all entries (default: last 30 days)
mood list

# List entries within a custom range
mood list --from-date 2024-06-01 --to-date 2024-06-30

# Reports
mood report distribution   # counts by mood
mood report streak         # longest same-mood run
mood report trend          # e.g. 7-day sliding summary

# Demo Script
bash run.sh   # seeds sample_data/entries_seed.json then prints all three reports

---

## 🎮 Usage

# CLI
# Add a new entry
mood add --mood happy --date 2024-06-26 --note "Lunch with friends"

# List all entries (default: last 30 days)
mood list

# List entries within a custom range
mood list --from 2024-06-01 --to 2024-06-30

# Reports
mood report distribution   # counts by mood
mood report streak         # longest same-mood run
mood report trend          # e.g. 7-day sliding summary


# Demo Script
bash run.sh
# Seeds sample_data/entries_seed.json then prints all three reports


## Project Structure 
Mood-Tracker/
├─ app/
│  ├─ models.py        # Entry dataclass
│  ├─ repository.py    # JSON/SQLite persistence
│  ├─ analytics.py     # distribution, streak, trend
│  └─ cli.py           # Click commands (controller layer)
├─ sample_data/
│  └─ entries_seed.json
├─ tests/
│  ├─ test_repository.py
│  └─ test_analytics.py
├─ run.sh              # one-line demo
├─ requirements.txt
└─ README.md


## Architecture
   [ CLI ]
      ↓
[ Controller ]           ← User input triggers
      ↓
[ Service / Analytics ]  ← Business logic (counts, streak, trend)
      ↓
[ Repository ]           ← JSON file or SQLite DB


## Running Tests

# From project root and with your virtualenv activated:
pytest --maxfail=1 --disable-warnings -q

# You can also view coverage (if you have pytest-cov):
pytest --cov=app
open htmlcov/index.html
