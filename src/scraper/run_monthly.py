from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path

from src.scraper.amazon_scraper import scrape_amazon_product
from src.scraper.db import (
    DEFAULT_DB_PATH,
    get_connection,
    init_db,
    insert_supplier_price,
)
from src.scraper.etl import SupplierPriceInput, build_supplier_price


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Monthly Amazon scraper.")
    parser.add_argument("--url", required=True, help="Amazon product URL")
    parser.add_argument("--item-name", default="Hojalicious Tea", help="Item label")
    parser.add_argument(
        "--quantity-count",
        type=int,
        default=None,
        help="Manual override for count (if missing on page)",
    )
    parser.add_argument(
        "--grams-total",
        type=float,
        default=None,
        help="Manual override for total grams (if missing on page)",
    )
    parser.add_argument(
        "--grams-per-unit",
        type=float,
        default=2.5,
        help="Assumed grams per tea bag when only count is available",
    )
    parser.add_argument(
        "--db-path",
        type=Path,
        default=DEFAULT_DB_PATH,
        help="SQLite database path",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run headless browser for scraping",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    scraped = scrape_amazon_product(args.url, headless=args.headless)

    supplier_input = SupplierPriceInput(
        item_name=args.item_name or scraped.item_name,
        total_price=scraped.total_price,
        quantity_count=args.quantity_count or scraped.quantity_count,
        grams_total=args.grams_total or scraped.grams_total,
        grams_per_unit=args.grams_per_unit,
    )
    grams_total, price_per_gram = build_supplier_price(supplier_input)

    conn = get_connection(args.db_path)
    init_db(conn)
    insert_supplier_price(
        conn=conn,
        date=date.today().isoformat(),
        item_name=supplier_input.item_name,
        total_price=supplier_input.total_price,
        quantity_count=supplier_input.quantity_count,
        grams_total=grams_total,
        price_per_gram=price_per_gram,
    )
    conn.close()

    print(
        f"Stored {supplier_input.item_name} price ${supplier_input.total_price:.2f} "
        f"({price_per_gram:.4f}/g)."
    )


if __name__ == "__main__":
    main()
