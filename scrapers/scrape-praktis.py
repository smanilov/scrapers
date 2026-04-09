#!/usr/bin/env python3

from scrape_common import HEADERS, scrape, run

URL = "https://praktis.bg/avto-i-velo-svyat/preporachitelno-oborudvane-za-avtomobil/kompresori-za-avtomobil"
CACHE_FILE = "cache/praktis_cache.html"
RESULT_FILE = "results/result-praktis.txt"


def get_cards(soup):
    # Each product appears 4× in the HTML; deduplicate by product ID.
    seen = set()
    result = []
    for box in soup.select('article[data-name^="pc:root:"]'):
        pid = box["data-name"].split(":")[-1]
        if pid not in seen:
            seen.add(pid)
            result.append(box)
    return result


def get_name(box):
    el = box.select_one('a[data-name^="pc:default-title:"] span')
    return el.get_text(strip=True) if el else None


def get_price(box):
    eur_val = box.select_one('span[data-name="price-info-regular-price-value"]')
    eur_cur = box.select_one('span[data-name="price-info-regular-price-currency"]')
    bgn_val = box.select_one('span[data-name="price-info-regular-price-eur-value"]')
    bgn_cur = box.select_one('span[data-name="price-info-regular-price-eur-currency"]')
    if not bgn_val or not bgn_cur:
        return None
    bgn = f"{bgn_val.get_text(strip=True)} {bgn_cur.get_text(strip=True)}"
    eur = f"{eur_val.get_text(strip=True)} {eur_cur.get_text(strip=True)}" if eur_val and eur_cur else None
    return f"{eur} | {bgn}" if eur else bgn


def scrape_page(cached=False):
    return scrape(URL, CACHE_FILE, HEADERS, cached, get_cards, get_name, get_price)


if __name__ == "__main__":
    run(RESULT_FILE, CACHE_FILE, scrape_page)
