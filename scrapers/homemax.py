#!/usr/bin/env python3

from common import HEADERS, scrape, run

URL = "https://www.home-max.bg/instrumenti-i-oborudvane/avtoprinadlejnosti/avtoinstrumenti/pompi-i-kompresori/"
CACHE_FILE = "cache/homemax.html"
RESULT_FILE = "results/homemax.txt"


def get_cards(soup):
    return soup.select("div.product-box-item")


def get_name(box):
    el = box.select_one(".product-box-title")
    return el.get_text(strip=True) if el else None


def get_price(box):
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
        return None
    return f"{eur} | {bgn}" if eur else bgn


def scrape_page(cached=False):
    return scrape(URL, CACHE_FILE, HEADERS, cached, get_cards, get_name, get_price)


if __name__ == "__main__":
    run(RESULT_FILE, CACHE_FILE, scrape_page, url=URL, headers=HEADERS)
