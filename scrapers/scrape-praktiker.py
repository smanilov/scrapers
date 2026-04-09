#!/usr/bin/env python3

from scrape_common import HEADERS, scrape, run

URL = "https://praktiker.bg/en/Avto-i-velo/Sigurnost-i-bezopasnost/Kompresori/c/P13060305?pageSize=92&currentPage=0"
CACHE_FILE = "cache/praktiker_cache.html"
RESULT_FILE = "results/result-praktiker.txt"


def get_cards(soup):
    return soup.select("te-product-box")


def get_name(box):
    return next(
        (a.get_text(strip=True) for a in box.select("a") if len(a.get_text(strip=True)) > 5),
        None,
    )


def get_price(box):
    def extract(currency_str, suffix):
        w = next((w for w in box.select(".price-wrapper") if any(currency_str in s for s in w.strings)), None)
        if not w:
            return None
        val = w.select_one(".product-price__value")
        return val.get_text(strip=True) + suffix if val else None

    bgn = extract("лв", " лв.")
    eur = extract("€", " €")
    if not bgn:
        return None
    return f"{eur} | {bgn}" if eur else bgn


def scrape_page(cached=False):
    return scrape(URL, CACHE_FILE, HEADERS, cached, get_cards, get_name, get_price)


if __name__ == "__main__":
    run(RESULT_FILE, CACHE_FILE, scrape_page)
