#!/usr/bin/env python3

import argparse
import requests
from bs4 import BeautifulSoup

URL = "https://www.masterhaus.bg/bg/products/mashini-i-instrumenti/stroitelna-tehnika-i-mashini/kompresori"
CACHE_FILE = "masterhaus_cache.html"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0",
}


def parse_price(el):
    if not el:
        return None
    whole = "".join(t for t in el.find_all(string=True, recursive=False)).strip()
    decimal = el.select_one("sup")
    currency = el.select_one("abbr")
    if not decimal or not currency:
        return None
    return f"{whole}.{decimal.get_text(strip=True)} {currency.get_text(strip=True)}"


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
    boxes = soup.select("li[data-id]")
    total_cards = len(boxes)

    products = []

    for box in boxes:
        name_el = box.select_one("h2 a")
        if not name_el:
            continue

        name = name_el.get_text(strip=True)
        eur = parse_price(box.select_one("span.price-actual"))
        bgn = parse_price(box.select_one("span.price-second"))
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

    with open("result-masterhaus.txt", "w", encoding="utf-8") as f:
        f.write("\n=== PRODUCTS ===\n")
        f.write(f"Parsed: {parsed_count} / {total_cards}\n")
        for name, price in products:
            f.write(f"{name} | {price}\n")

    print("\n=== SUMMARY ===")
    print(f"Total parsed: {parsed_count} / {total_cards}")
    print("\nSaved to result-masterhaus.txt")


if __name__ == "__main__":
    main()
