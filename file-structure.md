# File Structure

```
/Users/mac/Documents/boston-boba-supply-chain
├── README.md
├── prd.md
├── progress.md
├── file-structure.md
├── USAGE.md                    # 📘 How to run scripts
├── .gitignore                  # Git exclusion rules
├── data
│   ├── .gitkeep
│   └── boba_analytics.db       # SQLite database (not in Git)
└── src
    ├── __init__.py
    ├── cost_model.sql          # Database schema
    ├── scraper.py              # Entry point wrapper
    ├── scraper
    │   ├── __init__.py
    │   ├── amazon_scraper.py   # Web scraper
    │   ├── db.py               # Database operations
    │   ├── etl.py              # Data transformation
    │   ├── run_monthly.py      # Monthly price scraper
    │   ├── record_margin.py    # 📊 Record historical margins
    │   └── run_monthly_complete.py  # 🚀 All-in-one monthly workflow
    └── dashboard
        ├── __init__.py
        ├── app.py              # Streamlit dashboard
        ├── data_access.py      # Database queries for dashboard
        └── metrics.py          # Profit margin calculations
```

## Notes
- `data/` holds the SQLite database file (excluded from Git).
- `USAGE.md` contains complete instructions for running scripts.
- `run_monthly_complete.py` combines scraping + margin recording in one command.
