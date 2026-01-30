 # File Structure
 
```
/Users/mac/Documents/boston-boba-supply-chain
├── README.md
├── prd.md
├── progress.md
├── file-structure.md
├── data
│   └── .gitkeep
└── src
    ├── cost_model.sql
    ├── scraper.py
    ├── scraper
    │   ├── __init__.py
    │   ├── amazon_scraper.py
    │   ├── db.py
    │   ├── etl.py
    │   └── run_monthly.py
    └── dashboard
        ├── __init__.py
        ├── app.py
        ├── data_access.py
        └── metrics.py
```
 
 ## Notes
- `data/` holds the SQLite database file.
