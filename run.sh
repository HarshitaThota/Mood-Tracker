set -euo pipefail

# Seed the canonical file your CLI reads (entries.json)
echo "⏳ Seeding sample data → entries.json"
cp sample_data/entries_seed.json entries.json

# List all entries
echo
echo "📋 All entries (via list):"
python -m app.cli list

# Run stats (distribution + streak)
echo
echo "📊 Stats (distribution + streak):"
python -m app.cli stats