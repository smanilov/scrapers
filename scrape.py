#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import time

BASE_URL = "https://www.dshome.bg/boltove?page={}"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"
}

def scrape_page(page):
    url = BASE_URL.format(page)
    print(f"\n=== PAGE {page} ===")

    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        r.raise_for_status()
    except Exception as e:
        print(f"Error fetching page {page}: {e}")
        return []

    soup = BeautifulSoup(r.text, "html.parser")

    products = []

    # better selector
    cards = soup.select("a[href*='/boltove/']")

    for card in cards:
        name_el = card.select_one("h3")
        price_el = card.select_one("span.text-red-600")

        # skip broken entries
        if not name_el or not price_el:
            continue

        name = name_el.get_text(strip=True)
        price = price_el.get_text(strip=True)

        print(f"{name} | {price}")
        products.append((name, price))

    return products


def main():
    all_products = []

    with open("result.txt", "w", encoding="utf-8") as f:
        for page in range(1, 25):
            products = scrape_page(page)
            all_products.extend(products)

            f.write(f"\n=== PAGE {page} ===\n")
            for name, price in products:
                f.write(f"{name} | {price}\n")

            time.sleep(0.5)

    print("\nSaved to result.txt")


if __name__ == "__main__":
    main()
