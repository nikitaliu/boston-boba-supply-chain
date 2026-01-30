"""
Combined script: scrape supplier price AND record historical margin.
Run this once per month for complete data collection.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Complete monthly workflow: scrape + record margin."
    )
    parser.add_argument("--url", required=True, help="Amazon product URL")
    parser.add_argument(
        "--quantity-count",
        type=int,
        default=None,
        help="Manual override for count",
    )
    parser.add_argument(
        "--grams-total",
        type=float,
        default=None,
        help="Manual override for total grams",
    )
    parser.add_argument(
        "--grams-per-unit",
        type=float,
        default=2.5,
        help="Assumed grams per tea bag",
    )
    parser.add_argument(
        "--size",
        choices=["medium", "large"],
        default="medium",
        help="Cup size for margin recording",
    )
    parser.add_argument(
        "--daily-volume",
        type=int,
        default=100,
        help="Daily sales volume for margin recording",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    print("=" * 60)
    print("STEP 1: Scraping supplier price from Amazon...")
    print("=" * 60)

    # Build scraper command
    scraper_cmd = [
        sys.executable,
        "-m",
        "src.scraper.run_monthly",
        "--url",
        args.url,
        "--grams-per-unit",
        str(args.grams_per_unit),
    ]
    if args.quantity_count:
        scraper_cmd.extend(["--quantity-count", str(args.quantity_count)])
    if args.grams_total:
        scraper_cmd.extend(["--grams-total", str(args.grams_total)])

    # Run scraper
    result = subprocess.run(scraper_cmd)
    if result.returncode != 0:
        print("\n❌ Scraper failed. Aborting.")
        sys.exit(1)

    print("\n" + "=" * 60)
    print("STEP 2: Recording historical margin...")
    print("=" * 60)

    # Build margin recorder command
    margin_cmd = [
        sys.executable,
        "-m",
        "src.scraper.record_margin",
        "--size",
        args.size,
        "--daily-volume",
        str(args.daily_volume),
    ]

    # Run margin recorder
    result = subprocess.run(margin_cmd)
    if result.returncode != 0:
        print("\n❌ Margin recording failed.")
        sys.exit(1)

    print("\n" + "=" * 60)
    print("✓ Monthly workflow complete!")
    print("=" * 60)
    print("\nYou can now run the dashboard to see updated data:")
    print("  python -m streamlit run src/dashboard/app.py")


if __name__ == "__main__":
    main()
