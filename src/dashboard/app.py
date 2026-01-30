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
    st.set_page_config(
        page_title="Tea by the Sea - Analytics",
        page_icon="🌊",
        layout="wide"
    )
    
    # Custom CSS - Tea by the Sea Theme
    st.markdown("""
    <style>
        /* Brand Colors */
        :root {
            --brand-blue: #0047AB;
            --light-blue: #E3F2FD;
            --ocean-blue: #4A90E2;
        }
        
        /* Header with circular logo style */
        .main-header {
            background: linear-gradient(135deg, #0047AB 0%, #4A90E2 100%);
            padding: 1.5rem;
            border-radius: 15px;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 0 4px 6px rgba(0, 71, 171, 0.1);
        }
        
        .brand-circle {
            background-color: #0047AB;
            color: white;
            width: 80px;
            height: 80px;
            border-radius: 50%;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-size: 1rem;
            font-weight: bold;
            text-align: center;
            line-height: 1.2;
            margin-bottom: 0.5rem;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
        }
        
        /* Metric cards with ocean theme */
        [data-testid="stMetricValue"] {
            color: #0047AB;
            font-weight: 600;
        }
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0047AB 0%, #003d82 100%);
        }
        
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
            color: white;
        }
        
        /* Buttons and sliders */
        .stButton>button {
            background-color: #0047AB;
            color: white;
            border-radius: 20px;
        }
        
        /* Wave decoration */
        .wave-divider {
            height: 3px;
            background: linear-gradient(90deg, #0047AB 0%, #4A90E2 50%, #0047AB 100%);
            margin: 1rem 0;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Brand Header
    st.markdown("""
    <div class="main-header">
        <div class="brand-circle">TEA<br>BY THE<br>SEA</div>
        <h2 style="color: white; margin-top: 0.5rem;">Boston Profitability Dashboard</h2>
        <p style="color: #E3F2FD; margin-top: 0.5rem;">🌊 Your favorite bubble tea shop by the sea</p>
    </div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown("### 🎯 Scenario Controls")
    st.sidebar.markdown('<div class="wave-divider"></div>', unsafe_allow_html=True)
    
    size_label = st.sidebar.radio("🥤 Cup Size", ["Medium (500ml)", "Large (700ml)"])
    daily_volume = st.sidebar.slider("🧋 Daily Sales Volume", 0, 500, 100)

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

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 💰 Price Sensitivity")
    st.sidebar.markdown(
        f"🔴 **Real Scraped Price**: ${total_price:.2f}  \n"
        f"*(Last updated: {date.today().strftime('%Y-%m-%d')})*"
    )
    
    price_override = st.sidebar.slider(
        "Adjust Pack Price (USD)",
        min_value=0.0,
        max_value=max(50.0, total_price * 2),
        value=float(total_price),
        step=0.1,
        help=f"🔴 Real price: ${total_price:.2f} | Drag to simulate different scenarios"
    )
    
    # Show if user is at real price or simulating
    if abs(price_override - total_price) < 0.01:
        st.sidebar.success("✓ Currently at real scraped price")
    else:
        diff = price_override - total_price
        diff_pct = (diff / total_price) * 100
        if diff > 0:
            st.sidebar.warning(f"⚠️ +${diff:.2f} (+{diff_pct:.1f}%) above real price")
        else:
            st.sidebar.info(f"💡 ${abs(diff):.2f} ({abs(diff_pct):.1f}%) below real price")
    
    effective_price_per_gram = resolve_price_per_gram(price_override, grams_total)

    size_ml = SIZE_MEDIUM if size_label.startswith("Medium") else SIZE_LARGE
    price_per_cup = PRICE_MEDIUM if size_ml == SIZE_MEDIUM else PRICE_LARGE

    revenue = compute_revenue(price_per_cup, daily_volume)
    cogs = compute_cogs(effective_price_per_gram, size_ml, daily_volume)
    gross_margin = compute_gross_margin(revenue, cogs)
    total_profit = revenue - cogs

    st.markdown('<div class="wave-divider"></div>', unsafe_allow_html=True)
    st.subheader("📊 Today's Performance")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("💰 Profit Margin", f"{gross_margin:.2f}%")
    with col2:
        st.metric("🎯 Daily Profit", f"${total_profit:.2f}")
    with col3:
        st.metric("💵 Daily Revenue", f"${revenue:.2f}")
    with col4:
        st.metric("📦 Daily Cost", f"${cogs:.2f}")

    st.info(
        f"🍵 **Supplier**: {item_name} | "
        f"**Total Weight**: {grams_total:.1f}g | "
        f"**Price per Gram**: ${effective_price_per_gram:.4f}"
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

    st.markdown('<div class="wave-divider"></div>', unsafe_allow_html=True)
    st.subheader("📈 Profit Margin History")
    st.line_chart(history, x="date", y="gross_margin")


if __name__ == "__main__":
    main()
