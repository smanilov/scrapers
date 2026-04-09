#!/usr/bin/env python3

import argparse
import requests
from bs4 import BeautifulSoup

URL = "https://praktiker.bg/en/Avto-i-velo/Sigurnost-i-bezopasnost/Kompresori/c/P13060305?pageSize=92&currentPage=0"
CACHE_FILE = "praktiker_cache.html"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"
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
    boxes = soup.select("te-product-box")
    total_cards = len(boxes)

    products = []

    for box in boxes:
        name = next(
            (a.get_text(strip=True) for a in box.select("a") if len(a.get_text(strip=True)) > 5),
            None,
        )
        def extract(currency_str, suffix):
            w = next((w for w in box.select(".price-wrapper") if any(currency_str in s for s in w.strings)), None)
            if not w:
                return None
            val = w.select_one(".product-price__value")
            return val.get_text(strip=True) + suffix if val else None

        bgn = extract("лв", " лв.")
        eur = extract("€", " €")
        if not name or not bgn:
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

    with open("result-praktiker.txt", "w", encoding="utf-8") as f:
        f.write("\n=== PRODUCTS ===\n")
        f.write(f"Parsed: {parsed_count} / {total_cards}\n")
        for name, price in products:
            f.write(f"{name} | {price}\n")

    print("\n=== SUMMARY ===")
    print(f"Total parsed: {parsed_count} / {total_cards}")
    print("\nSaved to result-praktiker.txt")


if __name__ == "__main__":
    main()
