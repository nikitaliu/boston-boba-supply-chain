from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Optional

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


PRICE_RE = re.compile(r"\$?\s*([0-9]+(?:\.[0-9]{1,2})?)")
COUNT_RE = re.compile(r"([0-9]+)\s*(?:count|ct)\b", re.IGNORECASE)
WEIGHT_RE = re.compile(
    r"([0-9]+(?:\.[0-9]+)?)\s*(g|gram|grams|kg|oz|lb)\b", re.IGNORECASE
)


@dataclass(frozen=True)
class ScrapedProduct:
    item_name: str
    total_price: float
    quantity_count: Optional[int]
    grams_total: Optional[float]


def _parse_price(text: str) -> Optional[float]:
    match = PRICE_RE.search(text.replace(",", ""))
    if not match:
        return None
    return float(match.group(1))


def _parse_count(text: str) -> Optional[int]:
    match = COUNT_RE.search(text)
    if not match:
        return None
    return int(match.group(1))


def _parse_weight_grams(text: str) -> Optional[float]:
    match = WEIGHT_RE.search(text.replace(",", ""))
    if not match:
        return None
    value = float(match.group(1))
    unit = match.group(2).lower()
    if unit in ("g", "gram", "grams"):
        return value
    if unit == "kg":
        return value * 1000.0
    if unit == "oz":
        return value * 28.3495
    if unit == "lb":
        return value * 453.592
    return None


def _extract_title(driver: webdriver.Chrome) -> str:
    title = driver.find_element(By.ID, "productTitle")
    return title.text.strip()


def _extract_price(driver: webdriver.Chrome) -> Optional[float]:
    price_whole = driver.find_elements(By.CSS_SELECTOR, "span.a-price-whole")
    price_fraction = driver.find_elements(By.CSS_SELECTOR, "span.a-price-fraction")
    if price_whole:
        whole = price_whole[0].text.replace(",", "").strip()
        fraction = price_fraction[0].text.strip() if price_fraction else "00"
        return _parse_price(f"{whole}.{fraction}")

    price_block = driver.find_elements(By.ID, "priceblock_ourprice")
    if price_block:
        return _parse_price(price_block[0].text)

    price_alt = driver.find_elements(By.CSS_SELECTOR, "span.a-offscreen")
    if price_alt:
        return _parse_price(price_alt[0].text)

    return None


def _extract_details_text(driver: webdriver.Chrome) -> str:
    detail_sections = driver.find_elements(By.ID, "productDetails_techSpec_section_1")
    if detail_sections:
        return detail_sections[0].text

    bullet_section = driver.find_elements(By.ID, "detailBullets_feature_div")
    if bullet_section:
        return bullet_section[0].text

    return ""


def build_driver(headless: bool = True) -> webdriver.Chrome:
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=options)


def scrape_amazon_product(url: str, headless: bool = True) -> ScrapedProduct:
    driver = build_driver(headless=headless)
    try:
        driver.get(url)
        WebDriverWait(driver, 15).until(
            ec.presence_of_element_located((By.ID, "productTitle"))
        )

        item_name = _extract_title(driver)
        price = _extract_price(driver)
        details = _extract_details_text(driver)

        quantity_count = _parse_count(item_name) or _parse_count(details)
        grams_total = _parse_weight_grams(item_name) or _parse_weight_grams(details)

        if price is None:
            raise ValueError("Unable to detect price on the product page.")

        return ScrapedProduct(
            item_name=item_name,
            total_price=price,
            quantity_count=quantity_count,
            grams_total=grams_total,
        )
    finally:
        driver.quit()
