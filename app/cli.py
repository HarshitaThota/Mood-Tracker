import sys
from datetime import date
import click

from .service import add_entry, list_entries, get_distribution, get_streak

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
    entry = add_entry(mood=mood, d=d, note=note or None)
    click.echo(f"Added entry #{entry.id} → {entry.mood} on {entry.date}")

@cli.command("list")
@click.option("--from-date", type=str, help="Filter start (YYYY-MM-DD)")
@click.option("--to-date",   type=str, help="Filter end   (YYYY-MM-DD)")
@click.option("--mood",      type=str, help="Filter by mood label (happy/sad/etc.)")
def _list(from_date, to_date, mood):
    """List entries (optional date range and mood type)."""
    entries = list_entries(from_date, to_date, mood)
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
    dist = get_distribution(from_date, to_date)
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
    streaks = get_streak(from_date, to_date)
    if not streaks:
        click.echo("No entries in that span.")
        sys.exit(1)

    click.echo("Longest streak (days):")
    for mood, days in streaks.items():
        click.echo(f"  {mood:<7} : {days}")


if __name__ == "__main__":
    cli()
