import sys
from datetime import date
import click

from .models import Entry
from .repository import load_entries, save_entries, STORAGE
from .analytics import filter_by_date, distribution, longest_streak

@click.group()
def cli():
    """Daily Mood Tracker 📓"""
    pass

@cli.command()
@click.option("--mood", required=True, help="Mood label (happy/sad/etc.)")
@click.option("--date", "d", default=date.today().isoformat(), help="YYYY-MM-DD, default=today")
@click.option("--note", default="", help="Optional note")
def add(mood, d, note):
    """Add a new mood entry."""
    entries = load_entries()
    new_id = max((e.id for e in entries), default=0) + 1
    entry = Entry(
        id=new_id,
        mood=mood,
        date=date.fromisoformat(d),
        note=note or None
    )
    entries.append(entry)
    save_entries(entries)
    click.echo(f"Added entry #{new_id} → {mood} on {d}")

@cli.command("list")
@click.option("--from-date", type=str, help="Filter start (YYYY-MM-DD)")
@click.option("--to-date",   type=str, help="Filter end   (YYYY-MM-DD)")
def _list(from_date, to_date):
    """List entries (optional date range)."""
    entries = load_entries()
    df = date.fromisoformat(from_date) if from_date else None
    dt = date.fromisoformat(to_date)   if to_date   else None
    entries = filter_by_date(entries, df, dt)

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
    entries = load_entries()
    df = date.fromisoformat(from_date) if from_date else None
    dt = date.fromisoformat(to_date)   if to_date   else None
    entries = filter_by_date(entries, df, dt)

    if not entries:
        click.echo("No entries in that span.")
        sys.exit(1)

    dist = distribution(entries)
    click.echo("Mood distribution:")
    for mood, cnt in dist.items():
        click.echo(f"  {mood:<7} : {cnt}")

@report.command("streak")
@click.option("--from-date", "from_date", type=str, help="Start YYYY-MM-DD")
@click.option("--to-date",   "to_date",   type=str, help="End   YYYY-MM-DD")
def report_streak(from_date, to_date):
    """Show longest consecutive-day streak per mood."""
    entries = load_entries()
    df = date.fromisoformat(from_date) if from_date else None
    dt = date.fromisoformat(to_date)   if to_date   else None
    entries = filter_by_date(entries, df, dt)

    if not entries:
        click.echo("No entries in that span.")
        sys.exit(1)

    streaks = longest_streak(entries)
    click.echo("Longest streak (days):")
    for mood, days in streaks.items():
        click.echo(f"  {mood:<7} : {days}")

if __name__ == "__main__":
    cli()
