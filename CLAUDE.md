# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this project does

Scrapes bolt/fastener product listings (names and prices) from two sites:

- `dshome.bg/boltove` — paginating through 24 pages, output to `result.txt`
- `praktiker.bg` — compressors category, single page, output to `result-praktiker.txt`

## Running the scrapers

`run.sh` is the canonical entry point:

```bash
./run.sh <dshome|praktiker> [--cached]
```

Or directly:

```bash
python3 scrape-dshome.py [--cached]
python3 scrape-praktiker.py [--cached]
```

`--cached` reads from local HTML files instead of making network requests.

## Output format

Both scripts write in the same format:

```
=== PAGE N ===        # dshome (one per page); praktiker uses === PRODUCTS ===
Parsed: X / Y
Product name | price
```

Praktiker prices include both currencies: `name | 9.71 € | 18.99 лв.`

## Caching

Download cached HTML with the provided shell scripts:

```bash
./cache-dshome.sh       # saves dshome/page-1.html … page-24.html
./cache-praktiker.sh    # saves praktiker_cache.html
```

Then run with `--cached` to parse from disk.

## Dependencies

- `requests`
- `beautifulsoup4`

Install with: `pip install requests beautifulsoup4`

## Code structure

### scrape-dshome.py

- `scrape_page(page, cached=False)` — fetches or reads `dshome/page-{page}.html`; returns `(products, parsed_count, total_cards)`. Uses CSS selector `a[href*='/boltove/']` to find product cards, then `h3` for name and `span.text-red-600` for price.
- `main()` — parses `--cached` flag, loops pages 1–24, writes `result.txt`, sleeps 0.5s between live requests (skipped when cached).

### scrape-praktiker.py

- `scrape_page(cached=False)` — fetches or reads `praktiker_cache.html`; returns `(products, parsed_count, total_cards)`. Uses `te-product-box` for product cards, first long `<a>` text for name, `.price-wrapper` spans for EUR (`€`) and BGN (`лв.`) prices.
- `main()` — parses `--cached` flag, calls `scrape_page()`, writes `result-praktiker.txt`.

## Known limitations / TODOs

- Page count (24) for dshome is hardcoded; dynamic detection not implemented.
- Praktiker URL is hardcoded to the compressors category.
