# 🧬 Data Scraper Blueprint

A **reusable Python template** for building API-based data scrapers. Clone it, swap in your target API, and you've got a working scraper with SQLite storage, deduplication, search, and CSV export — in minutes.

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Template](https://img.shields.io/badge/Type-Blueprint-orange?style=for-the-badge)

---

## ✨ What You Get

- **Multi-source scraping** — register as many API sources as you need
- **SQLite storage** — persistent local database with automatic deduplication
- **Rich CLI output** — color-coded tables powered by [Rich](https://github.com/Textualize/rich)
- **Search** — find records by keyword across any column
- **CSV export** — one command to export everything
- **Pagination support** — example pattern for paginated APIs
- **Rate limiting** — built-in delays to be respectful to API providers

---

## 🚀 Quick Start

### 1. Clone the blueprint

```bash
git clone https://github.com/krisschumacher365-ctrl/data_scraper.git
cd data_scraper
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Customize for your target (see guide below)

### 4. Run it

```bash
python main.py scrape              # Scrape all sources
python main.py scrape <source>     # Scrape one source
python main.py list                # View all stored records
python main.py search <keyword>    # Search by keyword
python main.py stats               # Database statistics
python main.py export              # Export to CSV
```

---

## 📁 Project Structure

```
data_scraper/
├── main.py             # CLI entry point & commands
├── scraper.py          # API fetching logic (✏️ add your scrapers here)
├── database.py         # SQLite operations (✏️ define your schema here)
├── config.py           # API endpoints & settings (✏️ configure here)
├── requirements.txt    # Python dependencies
├── LICENSE             # MIT License
└── README.md           # You are here
```

---

## 🛠️ How to Adapt This Blueprint

Follow these **4 steps** to turn this template into a working scraper for any API:

### Step 1 → `config.py` — Set your API endpoints

```python
APIS = {
    "my_api": {
        "url": "https://api.example.com/v1/items",
        "description": "My data source",
    },
}
```

### Step 2 → `database.py` — Define your data schema

Edit the `CREATE TABLE` statement and column names to match the data you're collecting:

```python
TABLE_NAME = "products"  # or "articles", "listings", etc.

# Then update the CREATE TABLE columns:
#   field_1 → name
#   field_2 → price
#   field_3 → category
#   ...
```

### Step 3 → `scraper.py` — Write your scraper function

Map the API response fields to your database columns:

```python
def scrape_my_api() -> list[dict]:
    data = _get(APIS["my_api"]["url"]).json()
    records = []
    for item in data:
        records.append({
            "source":  "my_api",
            "field_1": item["name"],
            "field_2": item["price"],
            "field_3": item["category"],
            "url":     item["link"],
            "extra":   "",
            "date_scraped": datetime.now().isoformat(),
        })
    return records

# Register it:
SCRAPERS = {"my_api": scrape_my_api}
```

### Step 4 → `main.py` — Update the display table

Change the column headers in `_print_table()` to match your fields.

---

## 🏗️ Architecture

```
┌──────────────┐     HTTP GET      ┌──────────────┐
│  API Source 1 │◄──────────────────│              │
│  (JSON)      │──────────────────►│              │
└──────────────┘    raw data       │  scraper.py  │
                                   │              │
┌──────────────┐     HTTP GET      │  • _get()    │
│  API Source 2 │◄──────────────────│  • scrapers  │
│  (JSON)      │──────────────────►│  • registry  │
└──────────────┘    raw data       └──────┬───────┘
                                          │
                                    Normalized
                                    record dicts
                                          │
                                          ▼
                                   ┌──────────────┐
                                   │ database.py  │
                                   │   (SQLite)   │
                                   │              │
                                   │ • Dedup via  │
                                   │   unique idx │
                                   │ • Search     │
                                   │ • Export     │
                                   └──────┬───────┘
                                          │
                                          ▼
                                   ┌──────────────┐
                                   │   main.py    │
                                   │   (CLI)      │
                                   │              │
                                   │ • Rich table │
                                   │ • CSV export │
                                   │ • Stats      │
                                   └──────────────┘
```

---

## 🧰 Built With

- **Python 3.11+** — core language
- **[Requests](https://docs.python-requests.org/)** — HTTP client
- **[Rich](https://github.com/Textualize/rich)** — terminal formatting
- **SQLite** — zero-config embedded database (stdlib)

---

## 💡 Ideas for Extending

- Add **HTML scraping** with BeautifulSoup for non-API sites
- Add **browser automation** with Playwright/Selenium for JS-rendered pages
- Add **scheduling** with `cron` or `schedule` for periodic scrapes
- Add **API authentication** (API keys, OAuth) in the `_get()` helper
- Add **notifications** (email, Slack, Discord) when new records appear
- Swap SQLite for **PostgreSQL** or **MongoDB** for larger datasets

---

## 📝 License

MIT — see [LICENSE](LICENSE) for details.

---

<p align="center">
  <i>A reusable scraper blueprint — fork it, customize it, ship it 🚀</i>
</p>
