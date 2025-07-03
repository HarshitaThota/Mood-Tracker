set -euo pipefail

# Start fresh
echo "⏳ Resetting entries.json to empty array"
echo "[]" > entries.json

# Seed via CLI
echo "⏳ Adding demo entries"
mood add --mood happy   --date 2024-07-25 --note "Gym"
mood add --mood sad --date 2024-07-26 --note "Gloomy day"
mood add --mood happy --date 2024-07-28 --note "Project finished"

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
