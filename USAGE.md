# Usage Guide

## Monthly Data Collection Workflow

### Option 1: All-in-One Command (Recommended)

Run scraper + margin recording in one command:

```bash
python -m src.scraper.run_monthly_complete \
  --url "https://www.amazon.com/Hojalicious-Jasmine-Green-Espresso-100ct/dp/B0G58HQ913/" \
  --quantity-count 100 \
  --size medium \
  --daily-volume 100
```

### Option 2: Step-by-Step

```bash
# Step 1: Scrape supplier price
python -m src.scraper.run_monthly \
  --url "https://www.amazon.com/..." \
  --quantity-count 100

# Step 2: Record historical margin
python -m src.scraper.record_margin \
  --size medium \
  --daily-volume 100
```

---

## View Dashboard

After collecting data:

```bash
python -m streamlit run src/dashboard/app.py
```

Open browser to `http://localhost:8501`

---

## Parameters

### Scraper (`run_monthly`)
- `--url`: Amazon product URL (required)
- `--quantity-count`: Number of tea bags (if page doesn't show it)
- `--grams-total`: Total grams (if page doesn't show it)
- `--grams-per-unit`: Grams per tea bag (default: 2.5)

### Margin Recorder (`record_margin`)
- `--size`: Cup size - `medium` or `large` (default: medium)
- `--daily-volume`: Daily sales volume (default: 100)

---

## Database Location

All data stored in: `data/boba_analytics.db`

**⚠️ Important**: Do NOT commit `data/` to Git. It's already in `.gitignore`.

---

## Troubleshooting

### Dashboard shows "No data" on trend chart
- Run `python -m src.scraper.record_margin` to add today's margin data

### ModuleNotFoundError
- Make sure you're in the project root directory
- Use `python -m` (not just `python`) to run scripts

### Scraper fails
- Check if Amazon URL is correct
- Try adding `--quantity-count` manually if page doesn't show it
