set -euo pipefail

# Start fresh
echo "⏳ Resetting entries.json to empty array"
echo "[]" > entries.json

# Seed via CLI
echo "⏳ Adding demo entries"
mood add --mood happy   --date 2025-02-25 --note "Gym"
mood add --mood blissful  --date 2025-02-26 --note "Sunny day"
mood add --mood happy --date 2025-02-28 --note "Project finished"

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
