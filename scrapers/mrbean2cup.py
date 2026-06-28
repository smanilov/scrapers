#!/usr/bin/env python3

import argparse
import json
import os
import re
import requests

from common import HEADERS, write_results

URL = "https://mrbean2cup.co.uk/spare-parts/gaggia/gaggia-classic-v3-2019-ri9480"
API_URL = "https://mrbean2cup.co.uk/ProductManagerData/GetMachineProductDataJsonFrontEnd"
CACHE_FILE = "cache/mrbean2cup.json"
RESULT_FILE = "results/mrbean2cup.txt"


def get_category_id(html):
    """Extract machineCategoryId from the React data-props blob on the machine page."""
    m = re.search(r'"machineCategoryId"\s*:\s*(\d+)', html)
    return int(m.group(1)) if m else None


def fetch_json():
    """Fetch the machine page, read its category id, then POST for the parts JSON."""
    r = requests.get(URL, headers=HEADERS, timeout=10)
    r.raise_for_status()
    category_id = get_category_id(r.text)
    if category_id is None:
        print("Could not find machineCategoryId on page")
        return None
    body = (
        f"MachineCategoryId={category_id}&DiagramVisibleNameId=0"
        "&SearchText&ProductStaus&PageSize=1000&ViewMode=list&PageNumber=1"
    )
    headers = {
        **HEADERS,
        "Content-Type": "application/x-www-form-urlencoded",
        "X-Requested-With": "XMLHttpRequest",
    }
    r = requests.post(API_URL, headers=headers, data=body, timeout=10)
    r.raise_for_status()
    return r.text


def load_json(cached):
    if cached:
        with open(CACHE_FILE, encoding="utf-8") as f:
            return f.read()
    try:
        text = fetch_json()
    except Exception as e:
        print(f"Error fetching: {e}")
        return None
    if text is None:
        return None
    os.makedirs(os.path.dirname(CACHE_FILE) or ".", exist_ok=True)
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        f.write(text)
    return text


def scrape(cached=False):
    """Parts come from a JSON API (the page is React), so this parses JSON, not HTML."""
    print("\n=== PRODUCTS ===")
    text = load_json(cached)
    if text is None:
        return [], 0, 0
    cards = json.loads(text).get("ProductData") or []
    total_cards = len(cards)
    products = []
    for card in cards:
        name = (card.get("ProductName") or "").strip()
        price = (card.get("ProductPrice") or "").strip()
        if not name or not price:
            continue
        print(f"{name} | {price}")
        products.append((name, price))
    parsed_count = len(products)
    print(f"\nParsed: {parsed_count} / {total_cards}")
    return products, parsed_count, total_cards


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cached", action="store_true", help=f"Read from {CACHE_FILE} instead of fetching")
    parser.add_argument("--download", action="store_true", help=f"Fetch and save to {CACHE_FILE} without parsing")
    args = parser.parse_args()

    if args.download:
        if load_json(cached=False) is not None:
            print(f"Saved to {CACHE_FILE}")
        return

    products, parsed_count, total_cards = scrape(cached=args.cached)
    write_results(RESULT_FILE, products, parsed_count, total_cards)
    print("\n=== SUMMARY ===")
    print(f"Total parsed: {parsed_count} / {total_cards}")
    print(f"\nSaved to {RESULT_FILE}")


if __name__ == "__main__":
    main()
