#!/usr/bin/env python3

from common import HEADERS, scrape, run

URL = "https://www.masterhaus.bg/bg/products/mashini-i-instrumenti/stroitelna-tehnika-i-mashini/kompresori"
CACHE_FILE = "cache/masterhaus.html"
RESULT_FILE = "results/masterhaus.txt"


def _parse_price(el):
    if not el:
        return None
    whole = "".join(t for t in el.find_all(string=True, recursive=False)).strip()
    decimal = el.select_one("sup")
    currency = el.select_one("abbr")
    if not decimal or not currency:
        return None
    return f"{whole}.{decimal.get_text(strip=True)} {currency.get_text(strip=True)}"


def get_cards(soup):
    return soup.select("li[data-id]")


def get_name(box):
    el = box.select_one("h2 a")
    return el.get_text(strip=True) if el else None


def get_price(box):
    eur = _parse_price(box.select_one("span.price-actual"))
    bgn = _parse_price(box.select_one("span.price-second"))
    if not bgn:
        return None
    return f"{eur} | {bgn}" if eur else bgn


def scrape_page(cached=False):
    return scrape(URL, CACHE_FILE, HEADERS, cached, get_cards, get_name, get_price)


if __name__ == "__main__":
    run(RESULT_FILE, CACHE_FILE, scrape_page, url=URL, headers=HEADERS)
