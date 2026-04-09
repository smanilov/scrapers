#!/usr/bin/env python3

from scrape_common import HEADERS, scrape, run

URL = "https://bauhaus.bg/pompi-i-kompresori-za-gumi/c/1928"
CACHE_FILE = "cache/bauhaus_cache.html"
RESULT_FILE = "results/result-bauhaus.txt"


def get_cards(soup):
    return soup.select("div.product_holder")


def get_name(box):
    el = box.select_one("a.product-name")
    return el.get_text(strip=True) if el else None


def get_price(box):
    eur = bgn = None
    for row in box.select("div.product-price table tr"):
        whole = row.select_one("td.text-right")
        decimal = row.select_one("sup")
        currency = row.select_one("small")
        if not (whole and decimal and currency):
            continue
        value = whole.get_text(strip=True) + decimal.get_text(strip=True)
        cur = currency.get_text(strip=True)
        if "€" in cur:
            eur = f"{value} €"
        elif "лв" in cur.lower():
            bgn = f"{value} лв."
    if not bgn:
        return None
    return f"{eur} | {bgn}" if eur else bgn


def scrape_page(cached=False):
    return scrape(URL, CACHE_FILE, HEADERS, cached, get_cards, get_name, get_price)


if __name__ == "__main__":
    run(RESULT_FILE, CACHE_FILE, scrape_page)
