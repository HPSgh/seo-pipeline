# Automated SEO Analytics Pipeline

An end-to-end data pipeline that automatically extracts search performance data from the Google Search Console API, transforms it with Pandas, and stores it in a SQLite database for long-term historical analysis — with a terminal report view and a local browser dashboard.

> Unlike the native Google Search Console dashboard, this pipeline retains data indefinitely and enables custom SQL-based analysis — no manual exports required.

---

## Why This Project Exists

Google Search Console only displays data for the last 16 months and requires manual exports for any custom analysis. This pipeline solves both problems by automating extraction and storing results in a local database that grows over time.

---

## Architecture

```
Google Search Console API
        │
        ▼
  extract.py       ← Authenticates via OAuth 2.0 and pulls raw query/page data
        │
        ▼
  transform.py     ← Cleans data, enforces types, calculates custom metrics
        │
        ▼
  load.py          ← Loads DataFrame into SQLite database
        │
        ▼
  gsc_data.db      ← Local SQLite database for long-term historical storage
        │
        ├──────────────────────────┐
        ▼                          ▼
  query.py                   dashboard.py
  ← SQL reports               ← Visual browser
    in terminal                 dashboard (HTML)
```

---

## Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| Language | Python 3.13 | Core scripting |
| Extraction | Google Search Console API | Raw search performance data |
| Auth | OAuth 2.0 (google-auth-oauthlib) | Secure API authentication |
| Transformation | Pandas | Data cleaning and custom metrics |
| Storage | SQLite | Lightweight local database |
| Visualization | Chart.js | Browser-based dashboard charts |
| Containerization | Docker | Portable deployment |

---

## Project Structure

```
seo-pipeline/
├── main.py            # Pipeline entry point — runs all steps in sequence
├── auth.py            # OAuth 2.0 authentication and token management
├── extract.py         # GSC API data extraction
├── transform.py       # Pandas transformation and custom metrics
├── load.py            # SQLite loading and SQL querying
├── query.py           # Preset SQL reports printed in the terminal
├── dashboard.py       # Generates and opens a visual browser dashboard
├── requirements.txt   # Python dependencies
├── Dockerfile         # Container definition
├── .gitignore         # Excludes secrets and auto-generated files
└── README.md          # This file
```

> `credentials.json`, `token.json`, and `gsc_data.db` are auto-generated locally and excluded from version control.

---

## Custom Metrics

Beyond raw GSC data, the pipeline calculates:

| Metric | Formula | Purpose |
|---|---|---|
| `ctr_percent` | `ctr × 100` | Human-readable click-through rate |

More custom metrics can be added in `transform.py`.

---

## Getting Started

### Prerequisites
- Python 3.10+
- A Google account with Search Console access
- A verified property in Google Search Console

### 1. Clone the repository
```bash
git clone https://github.com/HPSgh/seo-pipeline.git
cd seo-pipeline
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add your Google credentials
- Create a project in [Google Cloud Console](https://console.cloud.google.com)
- Enable the **Search Console API**
- Create an **OAuth 2.0 Desktop App** credential
- Download and rename it to `credentials.json`
- Place it in the project root

### 5. Configure your target site
In `extract.py`, update the `site_url` variable to match your verified GSC property:
```python
# URL prefix property
site_url = 'https://yoursite.com/'

# Domain property
site_url = 'sc-domain:yoursite.com'
```

### 6. Run the pipeline
```bash
# Extract, transform, and load fresh data into SQLite
python main.py

# View SQL reports in the terminal
python query.py

# Open the visual dashboard in your browser
python dashboard.py
```

On first run, a browser window will open for Google OAuth authentication. After approving, a `token.json` file is saved so subsequent runs are fully automated.

---

## Switching to a Different Site

To point the pipeline at a different website:
1. Ensure your Google account has access to that site's Search Console property
2. Update `site_url` in `extract.py` to the exact property URL
3. Re-run `python main.py`

---

## Running with Docker

```bash
docker build -t seo-pipeline .
docker run seo-pipeline
```

---

## Author

**Htoo Pyae Shan**
Software Engineering Student | Aspiring Data Analyst
[GitHub](https://github.com/HPSgh)
