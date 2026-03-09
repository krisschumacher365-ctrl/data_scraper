"""Scraper module — fetches job listings from free APIs."""

import time
from datetime import datetime

import requests

from config import APIS, RATE_LIMIT_DELAY, REQUEST_TIMEOUT, USER_AGENT


def _get(url: str) -> requests.Response:
    """Make a GET request with standard headers."""
    headers = {"User-Agent": USER_AGENT, "Accept": "application/json"}
    resp = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
    resp.raise_for_status()
    return resp


# ---------------------------------------------------------------------------
#  RemoteOK   (https://remoteok.com/api)
# ---------------------------------------------------------------------------

def scrape_remoteok() -> list[dict]:
    """Fetch remote job listings from RemoteOK."""
    data = _get(APIS["remoteok"]["url"]).json()

    jobs: list[dict] = []
    for item in data:
        # First element is metadata, skip it
        if not isinstance(item, dict) or "position" not in item:
            continue

        jobs.append({
            "source":      "remoteok",
            "title":       item.get("position", ""),
            "company":     item.get("company", ""),
            "location":    item.get("location", "Remote"),
            "url":         item.get("url", ""),
            "tags":        ", ".join(item.get("tags", [])) if item.get("tags") else "",
            "salary":      _build_salary(item.get("salary_min"), item.get("salary_max")),
            "description": _clean_html(item.get("description", "")),
            "date_posted": item.get("date", ""),
            "date_scraped": datetime.now().isoformat(),
        })

    return jobs


# ---------------------------------------------------------------------------
#  Arbeitnow   (https://www.arbeitnow.com/api/job-board-api)
# ---------------------------------------------------------------------------

def scrape_arbeitnow(pages: int = 3) -> list[dict]:
    """Fetch job listings from Arbeitnow (paginated)."""
    jobs: list[dict] = []

    for page in range(1, pages + 1):
        url = f"{APIS['arbeitnow']['url']}?page={page}"
        data = _get(url).json()

        for item in data.get("data", []):
            jobs.append({
                "source":      "arbeitnow",
                "title":       item.get("title", ""),
                "company":     item.get("company_name", ""),
                "location":    item.get("location", ""),
                "url":         item.get("url", ""),
                "tags":        ", ".join(item.get("tags", [])) if item.get("tags") else "",
                "salary":      "",
                "description": _clean_html(item.get("description", "")),
                "date_posted": item.get("created_at", ""),
                "date_scraped": datetime.now().isoformat(),
            })

        # Respect rate limits
        if page < pages:
            time.sleep(RATE_LIMIT_DELAY)

        # Stop if no more pages
        if not data.get("links", {}).get("next"):
            break

    return jobs


# ---------------------------------------------------------------------------
#  Helpers
# ---------------------------------------------------------------------------

def _build_salary(min_val, max_val) -> str:
    """Format a salary range string."""
    if min_val and max_val:
        return f"${int(min_val):,} – ${int(max_val):,}"
    if min_val:
        return f"From ${int(min_val):,}"
    if max_val:
        return f"Up to ${int(max_val):,}"
    return ""


def _clean_html(text: str) -> str:
    """Strip common HTML tags for a simple plaintext preview."""
    import re
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    # Truncate long descriptions
    if len(text) > 1000:
        text = text[:1000] + "…"
    return text


# ---------------------------------------------------------------------------
#  Unified entry point
# ---------------------------------------------------------------------------

SCRAPERS = {
    "remoteok":  scrape_remoteok,
    "arbeitnow": scrape_arbeitnow,
}


def scrape_all() -> list[dict]:
    """Run every available scraper and return combined results."""
    all_jobs: list[dict] = []
    for name, func in SCRAPERS.items():
        try:
            jobs = func()
            all_jobs.extend(jobs)
        except Exception as exc:
            print(f"[!] Error scraping {name}: {exc}")
        time.sleep(RATE_LIMIT_DELAY)
    return all_jobs
