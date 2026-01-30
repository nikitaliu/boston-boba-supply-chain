from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import pandas as pd
import streamlit as st

from src.dashboard.data_access import load_latest_supplier_price, load_margin_history
from src.dashboard.metrics import compute_cogs, compute_gross_margin, compute_revenue


PRICE_MEDIUM = 5.88
PRICE_LARGE = 7.13
SIZE_MEDIUM = 500
SIZE_LARGE = 700
DEFAULT_GRAMS_TOTAL = 250.0
DEFAULT_PRICE_PER_GRAM = 0.05


def resolve_price_per_gram(
    price_override: float,
    grams_total: float,
) -> float:
    if grams_total <= 0:
        return DEFAULT_PRICE_PER_GRAM
    return price_override / grams_total


def main() -> None:
    st.set_page_config(page_title="Boba Profitability Dashboard", layout="wide")
    st.title("Boba Tea Unit Economics & Profitability Dashboard")

    st.sidebar.header("Scenario Controls")
    size_label = st.sidebar.radio("Cup Size", ["Medium (500ml)", "Large (700ml)"])
    daily_volume = st.sidebar.slider("Daily Sales Volume", 0, 500, 100)

    db_path = Path("data/boba_analytics.db")
    latest_price = load_latest_supplier_price(db_path)

    if latest_price:
        item_name, total_price, quantity_count, grams_total, price_per_gram = latest_price
        grams_total = grams_total or (
            quantity_count * 2.5 if quantity_count else DEFAULT_GRAMS_TOTAL
        )
    else:
        item_name = "Hojalicious Tea"
        total_price = 12.99
        grams_total = DEFAULT_GRAMS_TOTAL
        price_per_gram = DEFAULT_PRICE_PER_GRAM

    price_override = st.sidebar.slider(
        "Price Sensitivity (pack price, USD)",
        min_value=0.0,
        max_value=max(50.0, total_price * 2),
        value=float(total_price),
        step=0.1,
    )
    effective_price_per_gram = resolve_price_per_gram(price_override, grams_total)

    size_ml = SIZE_MEDIUM if size_label.startswith("Medium") else SIZE_LARGE
    price_per_cup = PRICE_MEDIUM if size_ml == SIZE_MEDIUM else PRICE_LARGE

    revenue = compute_revenue(price_per_cup, daily_volume)
    cogs = compute_cogs(effective_price_per_gram, size_ml, daily_volume)
    gross_margin = compute_gross_margin(revenue, cogs)
    total_profit = revenue - cogs

    st.subheader("Current Profitability Metrics")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Gross Profit Margin (%)", f"{gross_margin:.2f}%")
    with col2:
        st.metric("Total Daily Profit ($)", f"${total_profit:.2f}")
    with col3:
        st.metric("Daily Revenue ($)", f"${revenue:.2f}")
    with col4:
        st.metric("Daily COGS ($)", f"${cogs:.2f}")

    st.write(
        f"Latest supplier item: {item_name} | "
        f"Assumed grams total: {grams_total:.1f}g | "
        f"Effective price per gram: ${effective_price_per_gram:.4f}"
    )

    history = load_margin_history(db_path)
    if history.empty:
        history = pd.DataFrame(
            {
                "date": [date.today().strftime("%Y-%m-%d")],
                "size_ml": [size_ml],
                "daily_volume": [daily_volume],
                "gross_margin": [gross_margin],
            }
        )

    st.subheader("Gross Margin Trend")
    st.line_chart(history, x="date", y="gross_margin")


if __name__ == "__main__":
    main()
