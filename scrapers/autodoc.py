#!/usr/bin/env python3

import argparse
import os
import requests
from bs4 import BeautifulSoup
import time

BASE_URL = "https://www.autodoc.parts/car-accessories/car-jacks?page={}"
CACHE_DIR = "cache/autodoc"
LAST_PAGE = 42
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0"
}
NICE_DELAY = 2.0 # seconds
RETRY_DELAY = 5.0


def fetch_page(page):
    """Fetch page HTML with retry on 403."""
    retry_delay = RETRY_DELAY
    while True:
        try:
            r = requests.get(BASE_URL.format(page), headers=HEADERS, timeout=10)
            if r.status_code == 403:
                print(f"403 on page {page}, retrying in {retry_delay:.0f}s...")
                time.sleep(retry_delay)
                retry_delay = min(retry_delay * 2, 120)
                continue
            r.raise_for_status()
        except requests.HTTPError as e:
            print(f"Error fetching page {page}: {e}")
            return None
        return r.text


def scrape_page(page, cached=False):
    print(f"\n=== PAGE {page} ===")

    if cached:
        with open(f"{CACHE_DIR}/page-{page}.html", encoding="utf-8") as f:
            html = f.read()
    else:
        html = fetch_page(page)
        if html is None:
            return [], 0, 0

    soup = BeautifulSoup(html, "html.parser")

    cards = soup.select("div.listing-item")
    total_cards = len(cards)

    products = []

    for card in cards:
        name_el = card.select_one(".listing-item__name")
        price_el = card.select_one(".listing-item__price-new")

        if not name_el or not price_el:
            continue

        name = name_el.get_text(strip=True)
        price = " ".join(price_el.get_text().split())

        print(f"{name} | {price}")
        products.append((name, price))

    parsed_count = len(products)

    print(f"\nParsed: {parsed_count} / {total_cards}")

    return products, parsed_count, total_cards


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cached", action="store_true", help=f"Read from {CACHE_DIR}/ instead of fetching")
    parser.add_argument("--download", action="store_true", help=f"Fetch and save to {CACHE_DIR}/ without parsing")
    args = parser.parse_args()

    if args.download:
        os.makedirs(CACHE_DIR, exist_ok=True)
        for page in range(1, LAST_PAGE + 1):
            print(f"Downloading page {page}...")
            html = fetch_page(page)
            if html is not None:
                with open(f"{CACHE_DIR}/page-{page}.html", "w", encoding="utf-8") as f:
                    f.write(html)
            time.sleep(NICE_DELAY)
        return


    total_parsed_all = 0
    total_cards_all = 0

    with open("results/autodoc.txt", "w", encoding="utf-8") as f:
        for page in range(1, LAST_PAGE + 1):
            products, parsed_count, total_cards = scrape_page(page, cached=args.cached)

            total_parsed_all += parsed_count
            total_cards_all += total_cards

            f.write(f"\n=== PAGE {page} ===\n")
            f.write(f"Parsed: {parsed_count} / {total_cards}\n")

            for name, price in products:
                f.write(f"{name} | {price}\n")

            if not args.cached:
                time.sleep(NICE_DELAY)

    print("\n=== SUMMARY ===")
    print(f"Total parsed: {total_parsed_all} / {total_cards_all}")

    print("\nSaved to results/autodoc.txt")


if __name__ == "__main__":
    main()
