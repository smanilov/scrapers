#!/usr/bin/env python3

import argparse
import requests
from bs4 import BeautifulSoup

URL = "https://mr-bricolage.bg/instrumenti/avtoaksesoari/kompresori-pompi/c/006008021?pageSize=50"
CACHE_FILE = "mrbricolage_cache.html"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "bg,en;q=0.5",
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
    boxes = soup.select("div.product")
    total_cards = len(boxes)

    products = []

    for box in boxes:
        name_el = box.select_one("h2.product__title a")
        price_els = box.select("div.product__price-value")
        if not name_el or not price_els:
            continue

        name = name_el.get_text(strip=True)
        eur = next((p.get_text(strip=True) for p in price_els if "€" in p.get_text()), None)
        bgn = next((p.get_text(strip=True) for p in price_els if "ЛВ" in p.get_text(strip=True).upper()), None)
        if not bgn:
            continue

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

    with open("result-mrbricolage.txt", "w", encoding="utf-8") as f:
        f.write("\n=== PRODUCTS ===\n")
        f.write(f"Parsed: {parsed_count} / {total_cards}\n")
        for name, price in products:
            f.write(f"{name} | {price}\n")

    print("\n=== SUMMARY ===")
    print(f"Total parsed: {parsed_count} / {total_cards}")
    print("\nSaved to result-mrbricolage.txt")


if __name__ == "__main__":
    main()
