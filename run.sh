set -euo pipefail

# Start fresh
echo "⏳ Resetting entries.json to empty array"
echo "[]" > entries.json

# Seed via CLI
echo "⏳ Adding demo entries"
mood add --mood happy   --date 2025-06-25 --note "Gym"
mood add --mood sad     --date 2025-06-26 --note "Rainy day"
mood add --mood anxious --date 2025-06-27 --note "Project deadline"

# List all entries
echo
echo "📋 All entries (via list):"
mood list

# Distribution report
echo
echo "📊 Mood distribution report:"
mood report distribution

# Streak report
echo
echo "📊 Mood streak report:"
mood report streak
