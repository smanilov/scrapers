#!/usr/bin/env python3

from common import scrape, run

URL = "https://mr-bricolage.bg/instrumenti/avtoaksesoari/kompresori-pompi/c/006008021?pageSize=50"
CACHE_FILE = "cache/mrbricolage.html"
RESULT_FILE = "results/mrbricolage.txt"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "bg,en;q=0.5",
}


def get_cards(soup):
    return soup.select("div.product")


def get_name(box):
    el = box.select_one("h2.product__title a")
    return el.get_text(strip=True) if el else None


def get_price(box):
    price_els = box.select("div.product__price-value")
    eur = next((p.get_text(strip=True) for p in price_els if "€" in p.get_text()), None)
    bgn = next((p.get_text(strip=True) for p in price_els if "ЛВ" in p.get_text(strip=True).upper()), None)
    if not bgn:
        return None
    return f"{eur} | {bgn}" if eur else bgn


def scrape_page(cached=False):
    return scrape(URL, CACHE_FILE, HEADERS, cached, get_cards, get_name, get_price)


if __name__ == "__main__":
    run(RESULT_FILE, CACHE_FILE, scrape_page)
