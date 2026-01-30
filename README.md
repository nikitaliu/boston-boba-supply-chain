# Boston Boba Supply Chain Analysis

Automated profitability monitoring system for Tea by the Sea (Boston) - Pure Tea Series.

## Quick Start

### 1. Install Dependencies
```bash
pip install streamlit pandas selenium
```

### 2. Run Monthly Data Collection
```bash
python -m src.scraper.run_monthly_complete \
  --url "https://www.amazon.com/..." \
  --quantity-count 100
```

### 3. View Dashboard
```bash
python -m streamlit run src/dashboard/app.py
```

Open browser to `http://localhost:8501`

## Features

- 📊 Real-time gross profit margin calculation
- 💰 Total daily profit tracking
- 📈 Historical margin trend visualization
- 🎯 Interactive scenario modeling (sales volume, price sensitivity)
- 🔄 Automated monthly supplier price scraping

## Documentation

- [USAGE.md](USAGE.md) - Detailed usage instructions
- [prd.md](prd.md) - Product requirements document
- [progress.md](progress.md) - Development progress log
- [file-structure.md](file-structure.md) - Project structure

## Project Structure

```
boston-boba-supply-chain/
├── src/scraper/          # Data collection scripts
├── src/dashboard/        # Streamlit dashboard
└── data/                 # SQLite database (local only)
```

## Monthly Workflow

1. Scrape supplier price from Amazon
2. Record historical margin data
3. View updated trends in dashboard

See [USAGE.md](USAGE.md) for complete instructions.
