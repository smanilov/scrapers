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
        return [], 0, 0

    soup = BeautifulSoup(r.text, "html.parser")

    cards = soup.select("a[href*='/boltove/']")
    total_cards = len(cards)

    products = []

    for card in cards:
        name_el = card.select_one("h3")
        price_el = card.select_one("span.text-red-600")

        if not name_el or not price_el:
            continue

        name = name_el.get_text(strip=True)
        price = price_el.get_text(strip=True)

        print(f"{name} | {price}")
        products.append((name, price))

    parsed_count = len(products)

    print(f"\nParsed: {parsed_count} / {total_cards}")

    return products, parsed_count, total_cards


def main():
    total_parsed_all = 0
    total_cards_all = 0

    with open("result.txt", "w", encoding="utf-8") as f:
        for page in range(1, 25):
            products, parsed_count, total_cards = scrape_page(page)

            total_parsed_all += parsed_count
            total_cards_all += total_cards

            f.write(f"\n=== PAGE {page} ===\n")
            f.write(f"Parsed: {parsed_count} / {total_cards}\n")

            for name, price in products:
                f.write(f"{name} | {price}\n")

            time.sleep(0.5)

    print("\n=== SUMMARY ===")
    print(f"Total parsed: {total_parsed_all} / {total_cards_all}")

    print("\nSaved to result.txt")


if __name__ == "__main__":
    main()
