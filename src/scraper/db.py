import sqlite3
from pathlib import Path
from typing import Iterable, Optional, Tuple
 
 
DEFAULT_DB_PATH = Path("data/boba_analytics.db")
 
 
def get_connection(db_path: Path = DEFAULT_DB_PATH) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(db_path)
 
 
def init_db(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS supplier_prices (
            date TEXT NOT NULL,
            item_name TEXT NOT NULL,
            total_price REAL NOT NULL,
            quantity_count INTEGER,
            grams_total REAL,
            price_per_gram REAL NOT NULL
        );
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS historical_margins (
            date TEXT NOT NULL,
            size_ml INTEGER NOT NULL,
            daily_volume INTEGER NOT NULL,
            revenue REAL NOT NULL,
            cogs REAL NOT NULL,
            gross_margin REAL NOT NULL,
            price_per_gram REAL NOT NULL
        );
        """
    )
    conn.commit()
 
 
def insert_supplier_price(
    conn: sqlite3.Connection,
    date: str,
    item_name: str,
    total_price: float,
    quantity_count: Optional[int],
    grams_total: Optional[float],
    price_per_gram: float,
) -> None:
    conn.execute(
        """
        INSERT INTO supplier_prices
        (date, item_name, total_price, quantity_count, grams_total, price_per_gram)
        VALUES (?, ?, ?, ?, ?, ?);
        """,
        (date, item_name, total_price, quantity_count, grams_total, price_per_gram),
    )
    conn.commit()
 
 
def insert_historical_margin(
    conn: sqlite3.Connection,
    date: str,
    size_ml: int,
    daily_volume: int,
    revenue: float,
    cogs: float,
    gross_margin: float,
    price_per_gram: float,
) -> None:
    conn.execute(
        """
        INSERT INTO historical_margins
        (date, size_ml, daily_volume, revenue, cogs, gross_margin, price_per_gram)
        VALUES (?, ?, ?, ?, ?, ?, ?);
        """,
        (date, size_ml, daily_volume, revenue, cogs, gross_margin, price_per_gram),
    )
    conn.commit()
 
 
def get_latest_supplier_price(
    conn: sqlite3.Connection,
) -> Optional[Tuple[str, float, Optional[int], Optional[float], float]]:
    cursor = conn.execute(
        """
        SELECT item_name, total_price, quantity_count, grams_total, price_per_gram
        FROM supplier_prices
        ORDER BY date DESC
        LIMIT 1;
        """
    )
    return cursor.fetchone()
 
 
def get_supplier_price_history(
    conn: sqlite3.Connection,
) -> Iterable[Tuple[str, str, float]]:
    cursor = conn.execute(
        """
        SELECT date, item_name, price_per_gram
        FROM supplier_prices
        ORDER BY date ASC;
        """
    )
    return cursor.fetchall()
 
 
def get_historical_margins(
    conn: sqlite3.Connection,
) -> Iterable[Tuple[str, int, int, float]]:
    cursor = conn.execute(
        """
        SELECT date, size_ml, daily_volume, gross_margin
        FROM historical_margins
        ORDER BY date ASC;
        """
    )
    return cursor.fetchall()
