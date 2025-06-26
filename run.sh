set -euo pipefail

# Seed the canonical file your CLI reads
echo "⏳ Seeding sample data → entries.json"
cp sample_data/entries_seed.json entries.json

# List all entries
echo
echo "📋 All entries (via list):"
python -m app.cli list

# Distribution report
echo
echo "📊 Mood distribution report:"
python -m app.cli report distribution

# Streak report
echo
echo "📊 Mood streak report:"
python -m app.cli report streak
