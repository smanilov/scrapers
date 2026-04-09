#!/usr/bin/env python3

import argparse
import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0",
}


def load_html(url, cache_file, headers, cached):
    if cached:
        with open(cache_file, encoding="utf-8") as f:
            return f.read()
    try:
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
    except Exception as e:
        print(f"Error fetching: {e}")
        return None
    return r.text


def scrape(url, cache_file, headers, cached, get_cards, get_name, get_price):
    """Shared scraping loop: fetch HTML, iterate cards, extract name+price."""
    print("\n=== PRODUCTS ===")
    html = load_html(url, cache_file, headers, cached)
    if html is None:
        return [], 0, 0
    soup = BeautifulSoup(html, "html.parser")
    boxes = get_cards(soup)
    total_cards = len(boxes)
    products = []
    for box in boxes:
        name = get_name(box)
        price = get_price(box)
        if not name or not price:
            continue
        print(f"{name} | {price}")
        products.append((name, price))
    parsed_count = len(products)
    print(f"\nParsed: {parsed_count} / {total_cards}")
    return products, parsed_count, total_cards


def write_results(result_file, products, parsed_count, total_cards):
    with open(result_file, "w", encoding="utf-8") as f:
        f.write("\n=== PRODUCTS ===\n")
        f.write(f"Parsed: {parsed_count} / {total_cards}\n")
        for name, price in products:
            f.write(f"{name} | {price}\n")


def run(result_file, cache_file, scrape_fn):
    parser = argparse.ArgumentParser()
    parser.add_argument("--cached", action="store_true", help=f"Read from {cache_file} instead of fetching")
    args = parser.parse_args()
    products, parsed_count, total_cards = scrape_fn(cached=args.cached)
    write_results(result_file, products, parsed_count, total_cards)
    print("\n=== SUMMARY ===")
    print(f"Total parsed: {parsed_count} / {total_cards}")
    print(f"\nSaved to {result_file}")
