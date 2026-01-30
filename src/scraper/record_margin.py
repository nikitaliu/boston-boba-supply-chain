from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path

from src.scraper.db import (
    DEFAULT_DB_PATH,
    get_connection,
    get_latest_supplier_price,
    init_db,
    insert_historical_margin,
)


PRICE_MEDIUM = 5.88
PRICE_LARGE = 7.13
SIZE_MEDIUM = 500
SIZE_LARGE = 700
BREWING_RATIO_GRAMS = 105.0
BREWING_RATIO_ML = 4000.0


def grams_per_cup(size_ml: int) -> float:
    return (BREWING_RATIO_GRAMS / BREWING_RATIO_ML) * size_ml


def compute_revenue(price_per_cup: float, daily_volume: int) -> float:
    return price_per_cup * daily_volume


def compute_cogs(price_per_gram: float, size_ml: int, daily_volume: int) -> float:
    return grams_per_cup(size_ml) * price_per_gram * daily_volume


def compute_gross_margin(revenue: float, cogs: float) -> float:
    if revenue <= 0:
        return 0.0
    return ((revenue - cogs) / revenue) * 100.0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Record historical margin to database."
    )
    parser.add_argument(
        "--db-path",
        type=Path,
        default=DEFAULT_DB_PATH,
        help="SQLite database path",
    )
    parser.add_argument(
        "--size",
        choices=["medium", "large"],
        default="medium",
        help="Cup size for margin calculation",
    )
    parser.add_argument(
        "--daily-volume",
        type=int,
        default=100,
        help="Default daily sales volume",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    conn = get_connection(args.db_path)
    init_db(conn)

    # Get latest supplier price
    latest_price = get_latest_supplier_price(conn)
    if not latest_price:
        print("Error: No supplier price data found. Run scraper first.")
        conn.close()
        return

    item_name, total_price, quantity_count, grams_total, price_per_gram = latest_price

    # Determine size and price
    if args.size == "medium":
        size_ml = SIZE_MEDIUM
        price_per_cup = PRICE_MEDIUM
    else:
        size_ml = SIZE_LARGE
        price_per_cup = PRICE_LARGE

    # Calculate metrics
    revenue = compute_revenue(price_per_cup, args.daily_volume)
    cogs = compute_cogs(price_per_gram, size_ml, args.daily_volume)
    gross_margin = compute_gross_margin(revenue, cogs)

    # Insert into historical_margins
    insert_historical_margin(
        conn=conn,
        date=date.today().isoformat(),
        size_ml=size_ml,
        daily_volume=args.daily_volume,
        revenue=revenue,
        cogs=cogs,
        gross_margin=gross_margin,
        price_per_gram=price_per_gram,
    )

    conn.close()

    print(f"✓ Recorded margin for {date.today().isoformat()}")
    print(f"  Size: {args.size} ({size_ml}ml)")
    print(f"  Daily Volume: {args.daily_volume}")
    print(f"  Gross Margin: {gross_margin:.2f}%")
    print(f"  Revenue: ${revenue:.2f}")
    print(f"  COGS: ${cogs:.2f}")


if __name__ == "__main__":
    main()
