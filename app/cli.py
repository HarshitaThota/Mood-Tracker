import itertools
import sys
from datetime import date
import click

from .models import Entry
from .repository import load_entries, save_entries, STORAGE  # reuse constant
from .analytics import distribution, longest_streak, filter_by_date


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
    new_id = (max((e.id for e in entries), default=0) + 1)
    entry = Entry(id=new_id, mood=mood, date=date.fromisoformat(d), note=note or None)
    entries.append(entry)
    save_entries(entries)
    click.echo(f"Added entry #{new_id} → {mood} on {d}")


@cli.command("list")
@click.option("--from-date", type=str, help="Filter start (YYYY-MM-DD)")
@click.option("--to-date", type=str, help="Filter end (YYYY-MM-DD)")
def _list(from_date, to_date):
    """List entries (optional date range)."""
    entries = load_entries()
    df = date.fromisoformat(from_date) if from_date else None
    dt = date.fromisoformat(to_date) if to_date else None
    entries = filter_by_date(entries, df, dt)
    for e in entries:
        click.echo(f"{e.id:3} | {e.date} | {e.mood:<7} | {e.note or ''}")


@cli.command()
def stats():
    """Show distribution & longest streaks."""
    entries = load_entries()
    if not entries:
        click.echo("No data yet.")
        sys.exit()

    dist = distribution(entries)
    streaks = longest_streak(entries)

    click.echo("Mood distribution:")
    for m, cnt in dist.items():
        click.echo(f"  {m:<7} : {cnt}")

    click.echo("\nLongest streak (days):")
    for m, days in streaks.items():
        click.echo(f"  {m:<7} : {days}")


if __name__ == "__main__":
    cli()
