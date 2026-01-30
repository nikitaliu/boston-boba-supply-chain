from __future__ import annotations


BREWING_RATIO_GRAMS = 105.0
BREWING_RATIO_ML = 4000.0


def grams_per_cup(size_ml: int) -> float:
    return (BREWING_RATIO_GRAMS / BREWING_RATIO_ML) * size_ml


def compute_revenue(price_per_cup: float, daily_volume: int) -> float:
    return price_per_cup * daily_volume


def compute_cogs(
    price_per_gram: float,
    size_ml: int,
    daily_volume: int,
) -> float:
    return grams_per_cup(size_ml) * price_per_gram * daily_volume


def compute_gross_margin(revenue: float, cogs: float) -> float:
    if revenue <= 0:
        return 0.0
    return ((revenue - cogs) / revenue) * 100.0
