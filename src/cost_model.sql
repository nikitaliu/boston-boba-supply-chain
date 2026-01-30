CREATE TABLE IF NOT EXISTS supplier_prices (
    date TEXT NOT NULL,
    item_name TEXT NOT NULL,
    total_price REAL NOT NULL,
    quantity_count INTEGER,
    grams_total REAL,
    price_per_gram REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS historical_margins (
    date TEXT NOT NULL,
    size_ml INTEGER NOT NULL,
    daily_volume INTEGER NOT NULL,
    revenue REAL NOT NULL,
    cogs REAL NOT NULL,
    gross_margin REAL NOT NULL,
    price_per_gram REAL NOT NULL
);
