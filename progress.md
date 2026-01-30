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
 
## Next Task
- Add Login and Register buttons to the dashboard header.
- Reference: @prd.md (update requirements to include auth UI), then implement in `src/dashboard/app.py` using `st.columns` + `st.button` for alignment.
