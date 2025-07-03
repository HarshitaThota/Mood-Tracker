# Role: handle all I/O, user prompts, help text, and exit codes.
import sys
from datetime import date, datetime
import click

from .service import add_entry, list_entries, get_distribution, get_streak
from .repository import load_entries  # for duplicate‐date warning

# --- validation constraints ---
ALLOWED_MOODS = [
    "happy", "sad", "anxious", "excited",
    "bored", "angry", "irritated", "calm",
    "stressed", "motivated", "tired",
    "content", "surprised", "confused", "proud"
]
MAX_NOTE_LEN = 200


@click.group()
def cli():
    """Daily Mood Tracker 📓"""
    pass


@cli.command()
@click.option(
    "--mood", required=True,
    help=f"Mood label (choose from: {', '.join(ALLOWED_MOODS)})"
)
@click.option(
    "--date", "d",
    default=date.today().isoformat(),
    help="Date in YYYY-MM-DD format (default=today)"
)
@click.option(
    "--note",
    default="",
    help=f"Optional note (max {MAX_NOTE_LEN} characters)"
)
def add(mood, d, note):
    """Add a new mood entry with validation and duplicate‐date confirmation."""
    # 1) Validate mood
    mood_lower = mood.lower()
    if mood_lower not in ALLOWED_MOODS:
        raise click.BadParameter(
            f"Invalid mood. Please choose one of: {', '.join(ALLOWED_MOODS)}"
        )

    # 2) Validate & parse date
    try:
        entry_date = datetime.fromisoformat(d).date()
    except ValueError:
        raise click.BadParameter("Date must be in YYYY-MM-DD format.")
    if entry_date > date.today():
        raise click.BadParameter("Date cannot be in the future.")

    # 3) Validate note length
    if len(note) > MAX_NOTE_LEN:
        raise click.BadParameter(f"Note cannot exceed {MAX_NOTE_LEN} characters.")

    # 4) Duplicate-date confirmation
    existing = load_entries()
    if any(e.date == entry_date for e in existing):
        proceed = click.confirm(
            f"⚠️ An entry already exists for {entry_date}. "
            "Do you still want to add another entry for the same day?",
            default=False
        )
        if not proceed:
            click.echo("Aborted. No entry added.")
            sys.exit(0)

    # 5) Delegate to service layer
    entry = add_entry(mood=mood_lower, d=entry_date.isoformat(), note=note or None)
    click.echo(f"✅ Added entry #{entry.id} → {entry.mood} on {entry.date}")


def _parse_and_validate_dates(from_str: str, to_str: str):
    """Helper: parse ISO dates, ensure from ≤ to."""
    df = dt = None
    if from_str:
        try:
            df = datetime.fromisoformat(from_str).date()
        except ValueError:
            raise click.BadParameter("`--from-date` must be YYYY-MM-DD.")
    if to_str:
        try:
            dt = datetime.fromisoformat(to_str).date()
        except ValueError:
            raise click.BadParameter("`--to-date` must be YYYY-MM-DD.")
    if df and dt and df > dt:
        raise click.BadParameter("`--from-date` must be on or before `--to-date`.")
    return df, dt


@cli.command("list")
@click.option("--from-date", type=str, help="Filter start (YYYY-MM-DD)")
@click.option("--to-date",   type=str, help="Filter end   (YYYY-MM-DD)")
@click.option("--mood",      type=str, help="Filter by mood label (happy/sad/etc.)")
def _list(from_date, to_date, mood):
    """List entries (optional date range and mood type)."""
    # 1) parse & validate dates (you need to implement _parse_and_validate_dates)
    df, dt = _parse_and_validate_dates(from_date, to_date)

    # 2) validate mood filter
    mood_lower = mood.lower() if mood else None
    if mood_lower and mood_lower not in ALLOWED_MOODS:
        raise click.BadParameter(
            f"Invalid mood filter. \n Choose one of: \n {', '.join(ALLOWED_MOODS)}"
        )

    # 3) delegate to service
    entries = list_entries(
        date_from=df.isoformat() if df else None,
        date_to=dt.isoformat()   if dt else None,
        mood=mood_lower
    )

    # 4) output
    if not entries:
        click.echo("No entries found.")
        sys.exit(0)

    for e in entries:
        click.echo(f"{e.id:3} | {e.date} | {e.mood:<7} | {e.note or ''}")

@cli.group()
def report():
    """Generate mood reports."""
    pass


@report.command("distribution")
@click.option("--from-date", "from_date", type=str, help="Start YYYY-MM-DD")
@click.option("--to-date",   "to_date",   type=str, help="End   YYYY-MM-DD")
def report_distribution(from_date, to_date):
    """Show count of each mood in the given date range."""
    # parse & validate dates
    df, dt = _parse_and_validate_dates(from_date, to_date)

    dist = get_distribution(
        date_from=df.isoformat() if df else None,
        date_to=dt.isoformat()   if dt else None
    )
    if not dist:
        click.echo("No entries in that span.")
        sys.exit(1)

    click.echo("Mood distribution:")
    for mood, cnt in dist.items():
        click.echo(f"  {mood:<7} : {cnt}")


@report.command("streak")
@click.option("--from-date", "from_date", type=str, help="Start YYYY-MM-DD")
@click.option("--to-date",   "to_date",   type=str, help="End   YYYY-MM-DD")
def report_streak(from_date, to_date):
    """Show longest consecutive-day streak per mood."""
    # parse & validate dates
    df, dt = _parse_and_validate_dates(from_date, to_date)

    streaks = get_streak(
        date_from=df.isoformat() if df else None,
        date_to=dt.isoformat()   if dt else None
    )
    if not streaks:
        click.echo("No entries in that span.")
        sys.exit(1)

    click.echo("Longest streak (days):")
    for mood, days in streaks.items():
        click.echo(f"  {mood:<7} : {days}")


if __name__ == "__main__":
    cli()
