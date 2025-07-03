# Daily Mood Tracker

A small, fully-tested Python app for logging and analyzing your daily moods via:


---

## 🚀 Features

- **Add** a mood entry: date, mood type (happy, sad, anxious,…), optional note  
- **List** entries by date range
- **Reports**:  
  - **Distribution**: count of each mood  
  - **Streak**: your longest run of the same mood  
- **Storage**: JSON (no external DB) or SQLite (optional)  
- **Extensible**: easily swap-out storage, or package as a CLI tool

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



## 🎮 Usage
# Add a new entry
mood add --mood happy --date 2024-06-26 --note "Lunch with friends"

# List all entries
mood list
mood list --from-date 2024-06-01 --to-date 2024-06-30
mood list --mood happy
# List entries within a custom range and mood type
mood list --from-date 2025-06-01 --to-date 2025-06-10 --mood sad

# Reports
mood report distribution   # counts by mood
mood report streak         # longest same-mood run
# I collapsed multiple daily logs into the last mood of that day before computing streaks,
# preserving the user’s final sentiment.

# Demo Script
bash run.sh  
# seeds sample_data/entries_seed.json then prints all three reports

---

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
