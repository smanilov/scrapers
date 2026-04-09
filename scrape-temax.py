#!/usr/bin/env python3

from scrape_common import HEADERS, scrape, run

URL = "https://temax.bg/avto-i-velo-aksesoari/avtomobilni-prinadlezhnosti/PRODUCTAVTO-kompresor"
CACHE_FILE = "temax_cache.html"
RESULT_FILE = "result-temax.txt"


def get_cards(soup):
    return soup.select("li.product-item")


def get_name(box):
    el = box.select_one("a.product-item-link")
    return el.get_text(strip=True) if el else None


def get_price(box):
    eur_el = box.select_one("span.price")
    side_el = box.select_one("span.side-price")
    if not eur_el or not side_el:
        return None
    eur = eur_el.get_text(strip=True)
    bgn = "".join(t for t in side_el.find_all(string=True, recursive=False)).strip()
    if not bgn:
        return None
    return f"{eur} | {bgn}"


def scrape_page(cached=False):
    return scrape(URL, CACHE_FILE, HEADERS, cached, get_cards, get_name, get_price)


if __name__ == "__main__":
    run(RESULT_FILE, CACHE_FILE, scrape_page)
