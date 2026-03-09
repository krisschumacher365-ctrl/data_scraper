"""
Configuration — customize this file for your scraping target.

STEPS TO ADAPT:
  1. Set DB_NAME to something meaningful (e.g., "products.db", "articles.db")
  2. Replace the example API entries in APIS with your real endpoints
  3. Adjust REQUEST_TIMEOUT, USER_AGENT, and RATE_LIMIT_DELAY as needed
"""

import os

# ── Database ─────────────────────────────────────────────────────────────
DB_NAME = "data.db"                          # ← rename for your project
DB_PATH = os.path.join(os.path.dirname(__file__), DB_NAME)

# ── API Endpoints ────────────────────────────────────────────────────────
# Add one entry per data source you want to scrape.
# Each key becomes a CLI sub-command:  python main.py scrape <key>
APIS = {
    "example_api": {
        "url": "https://api.example.com/v1/data",
        "description": "Example — replace with a real API",
    },
    # "another_source": {
    #     "url": "https://other-api.com/items",
    #     "description": "Another data source",
    # },
}

# ── Request Settings ─────────────────────────────────────────────────────
REQUEST_TIMEOUT = 30          # seconds per request
USER_AGENT = "DataScraper/1.0 (Educational Project)"
RATE_LIMIT_DELAY = 2          # seconds between consecutive API calls
