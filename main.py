#!/usr/bin/env python3
"""
Job Listing Scraper — CLI entry point.

Usage:
    python main.py scrape              Scrape all sources and save to DB
    python main.py scrape remoteok     Scrape only RemoteOK
    python main.py scrape arbeitnow    Scrape only Arbeitnow
    python main.py list                Show all stored jobs
    python main.py search <keyword>    Search jobs by keyword
    python main.py stats               Show database statistics
    python main.py export              Export all jobs to jobs_export.csv
"""

import argparse
import csv
import sys

from rich.console import Console
from rich.table import Table

from database import get_all_jobs, get_job_count, init_db, insert_jobs, search_jobs
from scraper import SCRAPERS, scrape_all

console = Console()


# ── Commands ─────────────────────────────────────────────────────────────

def cmd_scrape(source: str | None = None) -> None:
    """Scrape job listings and store them."""
    with console.status("[bold green]Scraping jobs…") as status:
        if source:
            if source not in SCRAPERS:
                console.print(f"[red]Unknown source: {source}")
                console.print(f"Available: {', '.join(SCRAPERS)}")
                sys.exit(1)
            status.update(f"[bold green]Scraping {source}…")
            jobs = SCRAPERS[source]()
        else:
            jobs = scrape_all()

    console.print(f"\n[cyan]Fetched {len(jobs)} job listings.")

    inserted, duplicates = insert_jobs(jobs)
    console.print(f"[green]✓ Inserted: {inserted}  [yellow]⊘ Duplicates skipped: {duplicates}")
    console.print(f"[dim]Total jobs in database: {get_job_count()}")


def cmd_list() -> None:
    """Display all stored jobs in a table."""
    jobs = get_all_jobs()
    if not jobs:
        console.print("[yellow]No jobs in the database yet. Run 'scrape' first.")
        return
    _print_jobs_table(jobs)


def cmd_search(keyword: str) -> None:
    """Search for jobs matching a keyword."""
    jobs = search_jobs(keyword)
    if not jobs:
        console.print(f"[yellow]No jobs matching '{keyword}'.")
        return
    console.print(f"[cyan]Found {len(jobs)} matching jobs:\n")
    _print_jobs_table(jobs)


def cmd_stats() -> None:
    """Print quick database statistics."""
    jobs = get_all_jobs()
    if not jobs:
        console.print("[yellow]Database is empty.")
        return

    sources = {}
    for j in jobs:
        sources[j["source"]] = sources.get(j["source"], 0) + 1

    table = Table(title="Database Statistics")
    table.add_column("Source", style="cyan")
    table.add_column("Jobs", justify="right", style="green")
    for src, count in sorted(sources.items()):
        table.add_row(src, str(count))
    table.add_row("[bold]Total", f"[bold]{len(jobs)}")
    console.print(table)


def cmd_export() -> None:
    """Export all jobs to a CSV file."""
    jobs = get_all_jobs()
    if not jobs:
        console.print("[yellow]No jobs to export.")
        return

    filename = "jobs_export.csv"
    fields = ["source", "title", "company", "location", "url",
              "tags", "salary", "date_posted", "date_scraped"]
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(jobs)

    console.print(f"[green]✓ Exported {len(jobs)} jobs to {filename}")


# ── Helpers ──────────────────────────────────────────────────────────────

def _print_jobs_table(jobs: list[dict]) -> None:
    """Render a table of jobs to the console."""
    table = Table(show_lines=True)
    table.add_column("#", style="dim", width=4)
    table.add_column("Title", style="bold cyan", max_width=40)
    table.add_column("Company", style="green", max_width=25)
    table.add_column("Location", max_width=20)
    table.add_column("Tags", style="yellow", max_width=30)
    table.add_column("Salary", style="magenta", max_width=20)
    table.add_column("Source", style="dim")

    for i, job in enumerate(jobs, 1):
        table.add_row(
            str(i),
            job.get("title", ""),
            job.get("company", ""),
            job.get("location", ""),
            job.get("tags", "")[:60],
            job.get("salary", ""),
            job.get("source", ""),
        )

    console.print(table)
    console.print(f"[dim]Showing {len(jobs)} jobs\n")


# ── CLI ──────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Job Listing Scraper — fetch and store jobs from free APIs"
    )
    sub = parser.add_subparsers(dest="command")

    # scrape
    p_scrape = sub.add_parser("scrape", help="Scrape job listings")
    p_scrape.add_argument("source", nargs="?", default=None,
                          help="Specific source (remoteok, arbeitnow)")

    # list
    sub.add_parser("list", help="Show all stored jobs")

    # search
    p_search = sub.add_parser("search", help="Search by keyword")
    p_search.add_argument("keyword", help="Keyword to search for")

    # stats
    sub.add_parser("stats", help="Database statistics")

    # export
    sub.add_parser("export", help="Export jobs to CSV")

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
