 # Progress Log
 
 ## App Flow
 1. Monthly scraper runs and stores supplier price in SQLite.
 2. ETL calculates price per gram and appends historical metrics.
 3. Streamlit app reads SQLite and renders margin trends.
 4. User adjusts widgets to simulate daily volume and price sensitivity.
 
## Progress Updates
- Initialized project documentation (PRD, progress log, file structure doc).
- Implemented scraper modules, DB schema, and ETL utilities.
- Built Streamlit dashboard with widgets and margin chart.
- Ran scraper successfully and stored latest supplier price in SQLite.
- Started Streamlit app successfully on localhost.
- Errors encountered:
  - IndentationError in multiple modules due to leading whitespace.
  - Selenium cache permission error in sandbox.
  - Timeout loading product title when using Google search URL.
  - Missing grams/quantity data caused price-per-gram failure.
- Fixes applied:
  - Normalized file indentation.
  - Re-ran scraper and dashboard outside sandbox permissions.
  - Switched to direct Amazon product URL.
  - Added manual override args for `--quantity-count` and `--grams-total`.
 
## Structure Notes
- Dashboard supports size toggle, volume slider, and price sensitivity.
- Streamlit server runs at `http://localhost:8501` when launched.
- Dashboard now displays 4 profitability metrics in columns: Gross Profit Margin (%), Total Daily Profit ($), Daily Revenue ($), and Daily COGS ($).

## Latest Changes
- Added "Total Daily Profit ($)" metric card to show absolute dollar profit (responds to volume changes).
- Added "Daily Revenue ($)" and "Daily COGS ($)" metrics for complete profitability breakdown.
- Organized metrics into 4-column layout for better visibility.
- Created `src/scraper/record_margin.py` to automatically record historical margin data.
- Created `src/scraper/run_monthly_complete.py` for one-command monthly workflow.
- Updated dashboard to show today's date instead of "No data" when trend chart is empty.
- Created `USAGE.md` with complete instructions for running scripts.

## How to Use (Monthly Workflow)
1. Run complete workflow: `python -m src.scraper.run_monthly_complete --url "..." --quantity-count 100`
2. View dashboard: `python -m streamlit run src/dashboard/app.py`

## Next Task
- Test the complete monthly workflow end-to-end.
- Verify trend chart shows multiple data points after running margin recorder multiple times.
