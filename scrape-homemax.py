#!/usr/bin/env python3

import argparse
import requests
from bs4 import BeautifulSoup

URL = "https://www.home-max.bg/instrumenti-i-oborudvane/avtoprinadlejnosti/avtoinstrumenti/pompi-i-kompresori/"
CACHE_FILE = "homemax_cache.html"
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
    boxes = soup.select("div.product-box-item")
    total_cards = len(boxes)

    products = []

    for box in boxes:
        name_el = box.select_one(".product-box-title")
        if not name_el:
            continue

        name = name_el.get_text(strip=True)
        eur = bgn = None
        for wrapper in box.select(".price-item-wrapper"):
            holder = wrapper.select_one(".price-holder")
            currency_el = wrapper.select_one(".currency")
            if not (holder and currency_el):
                continue
            whole = "".join(t.strip() for t in holder.find_all(string=True, recursive=False))
            decimal = holder.select_one("sup")
            value = whole + (decimal.get_text(strip=True) if decimal else "")
            cur = currency_el.get_text(strip=True)
            if "€" in cur:
                eur = f"{value} €"
            elif "лв" in cur.lower():
                bgn = f"{value} {cur}"

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

    with open("result-homemax.txt", "w", encoding="utf-8") as f:
        f.write("\n=== PRODUCTS ===\n")
        f.write(f"Parsed: {parsed_count} / {total_cards}\n")
        for name, price in products:
            f.write(f"{name} | {price}\n")

    print("\n=== SUMMARY ===")
    print(f"Total parsed: {parsed_count} / {total_cards}")
    print("\nSaved to result-homemax.txt")


if __name__ == "__main__":
    main()
