#!/usr/bin/env python3
"""
Data Scraper Blueprint — CLI entry point.

Usage:
    python main.py scrape              Scrape all sources and save to DB
    python main.py scrape <source>     Scrape a specific source
    python main.py list                Show all stored records
    python main.py search <keyword>    Search records by keyword
    python main.py stats               Show database statistics
    python main.py export              Export all records to CSV

✏️  This is a generic template. Customize the table columns in
    _print_table() and the export fields in cmd_export() to match
    your database schema.
"""

import argparse
import csv
import sys

from rich.console import Console
from rich.table import Table

from database import (
    get_all_records,
    get_record_count,
    init_db,
    insert_records,
    search_records,
)
from scraper import SCRAPERS, scrape_all

console = Console()


# ── Commands ─────────────────────────────────────────────────────────────

def cmd_scrape(source: str | None = None) -> None:
    """Scrape data and store it."""
    with console.status("[bold green]Scraping…") as status:
        if source:
            if source not in SCRAPERS:
                console.print(f"[red]Unknown source: {source}")
                console.print(f"Available: {', '.join(SCRAPERS)}")
                sys.exit(1)
            status.update(f"[bold green]Scraping {source}…")
            records = SCRAPERS[source]()
        else:
            records = scrape_all()

    console.print(f"\n[cyan]Fetched {len(records)} records.")

    inserted, duplicates = insert_records(records)
    console.print(f"[green]✓ Inserted: {inserted}  [yellow]⊘ Duplicates skipped: {duplicates}")
    console.print(f"[dim]Total records in database: {get_record_count()}")


def cmd_list() -> None:
    """Display all stored records in a table."""
    records = get_all_records()
    if not records:
        console.print("[yellow]No records in the database yet. Run 'scrape' first.")
        return
    _print_table(records)


def cmd_search(keyword: str) -> None:
    """Search for records matching a keyword."""
    records = search_records(keyword)
    if not records:
        console.print(f"[yellow]No records matching '{keyword}'.")
        return
    console.print(f"[cyan]Found {len(records)} matching records:\n")
    _print_table(records)


def cmd_stats() -> None:
    """Print quick database statistics."""
    records = get_all_records()
    if not records:
        console.print("[yellow]Database is empty.")
        return

    sources: dict[str, int] = {}
    for r in records:
        sources[r["source"]] = sources.get(r["source"], 0) + 1

    table = Table(title="Database Statistics")
    table.add_column("Source", style="cyan")
    table.add_column("Records", justify="right", style="green")
    for src, count in sorted(sources.items()):
        table.add_row(src, str(count))
    table.add_row("[bold]Total", f"[bold]{len(records)}")
    console.print(table)


def cmd_export() -> None:
    """Export all records to a CSV file."""
    records = get_all_records()
    if not records:
        console.print("[yellow]No records to export.")
        return

    filename = "export.csv"
    # ✏️  CUSTOMIZE: list the columns you want in the CSV
    fields = ["source", "field_1", "field_2", "field_3", "url", "extra", "date_scraped"]
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(records)

    console.print(f"[green]✓ Exported {len(records)} records to {filename}")


# ── Helpers ──────────────────────────────────────────────────────────────

def _print_table(records: list[dict]) -> None:
    """
    Render a table of records to the console.
    ✏️  CUSTOMIZE: change columns to match your database schema.
    """
    table = Table(show_lines=True)
    table.add_column("#",       style="dim", width=4)
    table.add_column("Field 1", style="bold cyan", max_width=40)
    table.add_column("Field 2", style="green", max_width=25)
    table.add_column("Field 3", max_width=30)
    table.add_column("URL",     style="dim", max_width=30)
    table.add_column("Source",  style="yellow")

    for i, rec in enumerate(records, 1):
        table.add_row(
            str(i),
            rec.get("field_1", ""),
            rec.get("field_2", ""),
            rec.get("field_3", ""),
            rec.get("url", "")[:40],
            rec.get("source", ""),
        )

    console.print(table)
    console.print(f"[dim]Showing {len(records)} records\n")


# ── CLI ──────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Data Scraper Blueprint — fetch and store data from APIs"
    )
    sub = parser.add_subparsers(dest="command")

    # scrape
    p_scrape = sub.add_parser("scrape", help="Scrape data sources")
    p_scrape.add_argument("source", nargs="?", default=None,
                          help=f"Specific source ({', '.join(SCRAPERS)})")

    # list
    sub.add_parser("list", help="Show all stored records")

    # search
    p_search = sub.add_parser("search", help="Search by keyword")
    p_search.add_argument("keyword", help="Keyword to search for")

    # stats
    sub.add_parser("stats", help="Database statistics")

    # export
    sub.add_parser("export", help="Export records to CSV")

    args = parser.parse_args()

    # Initialize DB on every run
    init_db()

    match args.command:
        case "scrape":
            cmd_scrape(args.source)
        case "list":
            cmd_list()
        case "search":
            cmd_search(args.keyword)
        case "stats":
            cmd_stats()
        case "export":
            cmd_export()
        case _:
            parser.print_help()


if __name__ == "__main__":
    main()
