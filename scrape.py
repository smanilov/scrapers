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
    print(f"Fetching page {page}...")

    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        r.raise_for_status()
    except Exception as e:
        print(f"Error fetching page {page}: {e}")
        return []

    soup = BeautifulSoup(r.text, "html.parser")

    products = []

    # Each product is inside an <a> card
    cards = soup.select("a.bg-white.rounded-lg")

    for card in cards:
        name_el = card.select_one("h3")
        price_el = card.select_one("span.text-red-600")

        name = name_el.get_text(strip=True) if name_el else "N/A"
        price = price_el.get_text(strip=True) if price_el else "N/A"

        products.append((name, price))

    return products


def main():
    all_products = []

    for page in range(1, 25):  # pages 1–24
        products = scrape_page(page)
        all_products.extend(products)

        # be polite to server
        time.sleep(0.5)

    print("\n=== RESULTS ===\n")

    for name, price in all_products:
        print(f"{name} | {price}")


if __name__ == "__main__":
    main()
