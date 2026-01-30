 # PRD: Boba Tea Unit Economics & Profitability Dashboard
 
 ## 1. Overview
 Build an automated monthly monitoring system to analyze Gross Profit Margin for Tea by the Sea (Boston), focusing on the Pure Tea Series.
 
 ## 2. Scope
 - Products: Jasmine Green Tea, Classic Oolong Tea
 - Platform revenue source: UberEats only
 - Sizes: Medium (500ml), Large (700ml)
 - Exclusions: toppings, cheese foam, sugar/ice level, water cost, packaging cost
 
 ## 3. Business Logic
 ### 3.1 Pricing (Revenue, before tax)
 - Medium (500ml): $5.88
 - Large (700ml): $7.13
 
 ### 3.2 COGS
 - Supplier: Hojalicious (Amazon)
 - Brewing ratio: 105g tea grounds per 4000ml tea base
 - Cost inputs: ingredient unit cost only (from Amazon)
 
 ### 3.3 Key Metrics
 - Revenue = price_per_cup * daily_sales_volume
 - COGS = (grams_used_per_cup * price_per_gram) * daily_sales_volume
 - Gross Profit Margin = ((Revenue - COGS) / Revenue) * 100
 
 ## 4. Data Ingestion
 - Frequency: monthly
 - Target URL: Hojalicious Amazon product page
 - Tooling: Selenium or Playwright for dynamic content
 - Storage: SQLite `boba_analytics.db`
 - Tables:
   - `supplier_prices`: `date`, `item_name`, `total_price`, `quantity_count`, `price_per_gram`
   - `historical_margins`: monthly snapshots of calculated margins
 
 ## 5. Analytical Engine
 - Unit conversion: convert count/weight to grams
 - ETL: append monthly data into SQLite
 
 ## 6. Dashboard (Streamlit)
 - Entry command: `streamlit run src/dashboard/app.py`
 - Widgets:
   - Daily Sales Volume slider (0-500, default 100)
   - Price Sensitivity slider (override supplier price)
   - Size toggle: Medium (500ml) vs Large (700ml)
 - Visuals:
   - Line chart for monthly gross margin trend
   - Metric card for current gross margin
 
 ## 7. Future (Phase 2)
 - Milk-based teas
 - DoorDash comparison
 - Add cup/straw/water utility costs
