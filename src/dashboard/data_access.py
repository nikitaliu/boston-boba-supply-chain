from __future__ import annotations

from pathlib import Path
from typing import Optional, Tuple

import pandas as pd

from src.scraper.db import (
    DEFAULT_DB_PATH,
    get_connection,
    get_historical_margins,
    get_latest_supplier_price,
    init_db,
)


def load_latest_supplier_price(
    db_path: Path = DEFAULT_DB_PATH,
) -> Optional[Tuple[str, float, Optional[int], Optional[float], float]]:
    conn = get_connection(db_path)
    init_db(conn)
    result = get_latest_supplier_price(conn)
    conn.close()
    return result


def load_margin_history(db_path: Path = DEFAULT_DB_PATH) -> pd.DataFrame:
    conn = get_connection(db_path)
    init_db(conn)
    rows = list(get_historical_margins(conn))
    conn.close()
    return pd.DataFrame(
        rows,
        columns=["date", "size_ml", "daily_volume", "gross_margin"],
    )
