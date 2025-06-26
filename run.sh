set -euo pipefail

echo "⏳ Seeding sample data → data.json"
cp sample_data/entries_seed.json data.json

echo
echo "📋 All entries (via list):"
python -m app.cli list --file data.json

echo
echo "📊 Stats (distribution + streak):"
python -m app.cli stats --file data.json