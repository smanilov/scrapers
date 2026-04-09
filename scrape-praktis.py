#!/usr/bin/env python3

import argparse
import requests
from bs4 import BeautifulSoup

URL = "https://praktis.bg/avto-i-velo-svyat/preporachitelno-oborudvane-za-avtomobil/kompresori-za-avtomobil"
CACHE_FILE = "praktis_cache.html"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0",
}


def scrape_page(cached=False):
    print("\n=== PRODUCTS ===")

    if cached:
        with open(CACHE_FILE, encoding="utf-8") as f:
            html = f.read()
    else:
        try:
            r = requests.get(URL, headers=HEADERS, timeout=10)
            r.raise_for_status()
        except Exception as e:
            print(f"Error fetching: {e}")
            return [], 0, 0
        html = r.text

    soup = BeautifulSoup(html, "html.parser")
    all_boxes = soup.select('article[data-name^="pc:root:"]')
    seen = set()
    boxes = []
    for box in all_boxes:
        pid = box["data-name"].split(":")[-1]
        if pid not in seen:
            seen.add(pid)
            boxes.append(box)
    total_cards = len(boxes)

    products = []

    for box in boxes:
        name_el = box.select_one('a[data-name^="pc:default-title:"] span')
        if not name_el:
            continue

        name = name_el.get_text(strip=True)
        eur_val = box.select_one('span[data-name="price-info-regular-price-value"]')
        eur_cur = box.select_one('span[data-name="price-info-regular-price-currency"]')
        bgn_val = box.select_one('span[data-name="price-info-regular-price-eur-value"]')
        bgn_cur = box.select_one('span[data-name="price-info-regular-price-eur-currency"]')

        if not bgn_val or not bgn_cur:
            continue

        bgn = f"{bgn_val.get_text(strip=True)} {bgn_cur.get_text(strip=True)}"
        eur = f"{eur_val.get_text(strip=True)} {eur_cur.get_text(strip=True)}" if eur_val and eur_cur else None

        price = f"{eur} | {bgn}" if eur else bgn
        print(f"{name} | {price}")
        products.append((name, price))

    parsed_count = len(products)
    print(f"\nParsed: {parsed_count} / {total_cards}")

    return products, parsed_count, total_cards


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cached", action="store_true", help=f"Read from {CACHE_FILE} instead of fetching")
    args = parser.parse_args()

    products, parsed_count, total_cards = scrape_page(cached=args.cached)

    with open("result-praktis.txt", "w", encoding="utf-8") as f:
        f.write("\n=== PRODUCTS ===\n")
        f.write(f"Parsed: {parsed_count} / {total_cards}\n")
        for name, price in products:
            f.write(f"{name} | {price}\n")

    print("\n=== SUMMARY ===")
    print(f"Total parsed: {parsed_count} / {total_cards}")
    print("\nSaved to result-praktis.txt")


if __name__ == "__main__":
    main()
