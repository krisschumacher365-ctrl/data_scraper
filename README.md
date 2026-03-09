# 🕵️ Job Listing Scraper

A Python-based job listing scraper that fetches real-time job postings from **free public APIs** and stores them in a local **SQLite** database. Built as an AI-assisted speed project — concept to working tool in under 5 minutes.

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

---

## ✨ Features

- **Multi-source scraping** — pulls from [RemoteOK](https://remoteok.com) and [Arbeitnow](https://www.arbeitnow.com) APIs
- **SQLite storage** — persistent local database with automatic deduplication
- **Rich CLI output** — color-coded tables powered by [Rich](https://github.com/Textualize/rich)
- **Search** — find jobs by keyword across titles, companies, and tags
- **CSV export** — one command to export everything to a spreadsheet
- **Zero API keys** — works out of the box with free, open APIs
- **Rate limiting** — built-in delays to be respectful to API providers

---

## 📸 Demo

```
$ python main.py scrape

Fetched 399 job listings.
✓ Inserted: 394  ⊘ Duplicates skipped: 5
Total jobs in database: 394
```

```
$ python main.py stats

        Database Statistics
┏━━━━━━━━━━━┳━━━━━━┓
┃ Source    ┃ Jobs ┃
┡━━━━━━━━━━━╇━━━━━━┩
│ arbeitnow │  295 │
│ remoteok  │   99 │
│ Total     │  394 │
└───────────┴──────┘
```

```
$ python main.py search python

Found 4 matching jobs:
┏━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━┓
┃ #    ┃ Title              ┃ Company    ┃ Location ┃ Tags             ┃ Salary ┃ Source   ┃
┡━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━┩
│ 1    │ Backend Developer  │ AutoDS     │ Remote   │ python, backend  │        │ remoteok │
│ 2    │ Senior DevOps Eng  │ ChowNow    │ Remote   │ python, ansible  │        │ remoteok │
│ ...  │                    │            │          │                  │        │          │
└──────┴────────────────────┴────────────┴──────────┴──────────────────┴────────┴──────────┘
```

---

## 🚀 Quick Start

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/job-scraper.git
cd job-scraper
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run it

```bash
python main.py scrape       # Fetch jobs from all sources
python main.py list         # View all stored jobs
python main.py search AI    # Search by keyword
python main.py stats        # Database statistics
python main.py export       # Export to CSV
```

---

## 📁 Project Structure

```
job-scraper/
├── main.py             # CLI entry point & commands
├── scraper.py          # API fetching logic (RemoteOK, Arbeitnow)
├── database.py         # SQLite operations (insert, search, dedup)
├── config.py           # API endpoints & settings
├── requirements.txt    # Python dependencies
├── LICENSE             # MIT License
└── README.md           # You are here
```

---

## 🛠️ How It Works

```
┌──────────────┐     HTTP GET      ┌──────────────┐
│  RemoteOK    │◄──────────────────│              │
│  (JSON API)  │──────────────────►│              │
└──────────────┘    Job listings   │   scraper.py │
                                   │              │
┌──────────────┐     HTTP GET      │              │
│  Arbeitnow   │◄──────────────────│              │
│  (JSON API)  │──────────────────►│              │
└──────────────┘    Job listings   └──────┬───────┘
                                          │
                                    Normalized
                                    job dicts
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
                                   └──────────────┘
```

---

## 📊 Available Data Sources

| Source | Type | Auth Required | Jobs Per Fetch |
|--------|------|:---:|:---:|
| [RemoteOK](https://remoteok.com/api) | Remote jobs | ❌ None | ~100 |
| [Arbeitnow](https://www.arbeitnow.com/api/job-board-api) | EU job board | ❌ None | ~300 |

---

## 🧰 Built With

- **Python 3.11+** — core language
- **[Requests](https://docs.python-requests.org/)** — HTTP client
- **[Rich](https://github.com/Textualize/rich)** — terminal tables & formatting
- **SQLite** — zero-config embedded database (via Python stdlib)
- **GitHub Copilot** — AI-assisted development

---

## 📝 License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.

---

<p align="center">
  <i>Built with AI assistance in under 5 minutes ⚡</i>
</p>
