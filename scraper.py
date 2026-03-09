"""
Scraper module — fetches data from APIs.

STEPS TO ADAPT:
  1. Write one scrape_xxx() function per data source
  2. Each function should return a list of dicts matching your DB columns
  3. Register every scraper in the SCRAPERS dict at the bottom
  4. (Optional) add pagination, auth headers, or HTML parsing as needed
"""

import time
from datetime import datetime

import requests

from config import APIS, RATE_LIMIT_DELAY, REQUEST_TIMEOUT, USER_AGENT


# ── HTTP Helper ──────────────────────────────────────────────────────────

def _get(url: str, params: dict | None = None) -> requests.Response:
    """Make a GET request with standard headers."""
    headers = {"User-Agent": USER_AGENT, "Accept": "application/json"}
    resp = requests.get(url, headers=headers, params=params, timeout=REQUEST_TIMEOUT)
    resp.raise_for_status()
    return resp


# ── Utility Helpers ──────────────────────────────────────────────────────

def _clean_html(text: str) -> str:
    """Strip common HTML tags for a simple plaintext preview."""
    import re
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) > 1000:
        text = text[:1000] + "…"
    return text


# ---------------------------------------------------------------------------
#  ✏️  EXAMPLE SCRAPER — replace with your own
# ---------------------------------------------------------------------------

def scrape_example_api() -> list[dict]:
    """
    Fetch data from the example API.

    ✏️  CUSTOMIZE: replace this with real logic for your target API.
    The returned dicts MUST have keys matching your database columns.
    """
    data = _get(APIS["example_api"]["url"]).json()

    records: list[dict] = []
    for item in data:
        records.append({
            "source":       "example_api",
            "field_1":      item.get("name", ""),       # ← map to your fields
            "field_2":      item.get("category", ""),
            "field_3":      item.get("value", ""),
            "url":          item.get("url", ""),
            "extra":        "",
            "date_scraped": datetime.now().isoformat(),
        })

    return records


# ---------------------------------------------------------------------------
#  ✏️  EXAMPLE PAGINATED SCRAPER — shows pagination pattern
# ---------------------------------------------------------------------------

def scrape_paginated_example(pages: int = 3) -> list[dict]:
    """
    Fetch data from a paginated API.

    ✏️  CUSTOMIZE: replace the URL, field mapping, and pagination logic.
    """
    records: list[dict] = []

    for page in range(1, pages + 1):
        url = f"{APIS['example_api']['url']}?page={page}"
        data = _get(url).json()

        for item in data.get("results", []):
            records.append({
                "source":       "example_api",
                "field_1":      item.get("title", ""),
                "field_2":      item.get("author", ""),
                "field_3":      _clean_html(item.get("description", "")),
                "url":          item.get("link", ""),
                "extra":        "",
                "date_scraped": datetime.now().isoformat(),
            })

        # Respect rate limits between pages
        if page < pages:
            time.sleep(RATE_LIMIT_DELAY)

        # Stop if no more pages
        if not data.get("next"):
            break

    return records


# ---------------------------------------------------------------------------
#  Scraper Registry — add every scraper function here
# ---------------------------------------------------------------------------

SCRAPERS = {
    "example_api": scrape_example_api,
    # "paginated":  scrape_paginated_example,
    # "your_source": scrape_your_source,
}


def scrape_all() -> list[dict]:
    """Run every registered scraper and return combined results."""
    all_records: list[dict] = []
    for name, func in SCRAPERS.items():
        try:
            records = func()
            all_records.extend(records)
        except Exception as exc:
            print(f"[!] Error scraping {name}: {exc}")
        time.sleep(RATE_LIMIT_DELAY)
    return all_records
        time.sleep(RATE_LIMIT_DELAY)
    return all_jobs
