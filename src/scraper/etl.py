from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class SupplierPriceInput:
    item_name: str
    total_price: float
    quantity_count: Optional[int]
    grams_total: Optional[float]
    grams_per_unit: float


def calculate_grams_total(
    quantity_count: Optional[int],
    grams_total: Optional[float],
    grams_per_unit: float,
) -> Optional[float]:
    if grams_total:
        return grams_total
    if quantity_count:
        return quantity_count * grams_per_unit
    return None


def calculate_price_per_gram(total_price: float, grams_total: Optional[float]) -> float:
    if not grams_total or grams_total <= 0:
        raise ValueError("grams_total must be positive to compute price_per_gram.")
    return total_price / grams_total


def build_supplier_price(
    payload: SupplierPriceInput,
) -> tuple[Optional[float], float]:
    grams_total = calculate_grams_total(
        payload.quantity_count,
        payload.grams_total,
        payload.grams_per_unit,
    )
    price_per_gram = calculate_price_per_gram(payload.total_price, grams_total)
    return grams_total, price_per_gram
