"""Configuration for the job listing scraper."""

import os

# Database
DB_PATH = os.path.join(os.path.dirname(__file__), "jobs.db")

# API endpoints (no auth required)
APIS = {
    "remoteok": {
        "url": "https://remoteok.com/api",
        "description": "Remote OK - Remote job listings",
    },
    "arbeitnow": {
        "url": "https://www.arbeitnow.com/api/job-board-api",
        "description": "Arbeitnow - Job board listings",
    },
}

# Request settings
REQUEST_TIMEOUT = 30  # seconds
USER_AGENT = "JobScraper/1.0 (Educational Project)"
RATE_LIMIT_DELAY = 2  # seconds between API calls
