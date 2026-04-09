# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this project does

Scrapes product listings (names and prices) from five sites:

- `dshome.bg/boltove` — bolts/fasteners, 24 pages, output to `result-dshome.txt`
- `praktiker.bg` — compressors, single page, output to `result-praktiker.txt`
- `mr-bricolage.bg` — compressors, single page, output to `result-mrbricolage.txt`
- `bauhaus.bg` — compressors/pumps, single page, output to `result-bauhaus.txt`
- `home-max.bg` — compressors/pumps, single page, output to `result-homemax.txt`

## Running the scrapers

`run.sh` is the canonical entry point:

```bash
./run.sh <dshome|praktiker|mrbricolage|bauhaus|homemax> [--cached]
```

Or directly:

```bash
python3 scrape-dshome.py [--cached]
python3 scrape-praktiker.py [--cached]
python3 scrape-mrbricolage.py [--cached]
python3 scrape-bauhaus.py [--cached]
python3 scrape-homemax.py [--cached]
```

`--cached` reads from local HTML files instead of making network requests.

## Output format

All scripts write in the same format:

```
=== PAGE N ===        # dshome (one per page); others use === PRODUCTS ===
Parsed: X / Y
Product name | price
```

All scripts report both currencies: `name | 9.71 € | 18.99 лв.`

Note: home-max.bg displays round prices with a dash for cents (e.g. `17.- ЛВ.`), reported as-is.

## Caching

Download cached HTML with `cache.sh`:

```bash
./cache.sh dshome       # saves dshome/page-1.html … page-24.html
./cache.sh praktiker    # saves praktiker_cache.html
./cache.sh mrbricolage  # saves mrbricolage_cache.html
./cache.sh bauhaus      # saves bauhaus_cache.html
./cache.sh homemax      # saves homemax_cache.html
```

All targets use `-L` (follow redirects) and a realistic Firefox user-agent. mr-bricolage additionally sends `Accept` and `Accept-Language` headers required for SSR rendering.

Then run with `--cached` to parse from disk.

## Dependencies

- `requests`
- `beautifulsoup4`

Install with: `pip install requests beautifulsoup4`

## Code structure

All scripts follow the same structure:

- `scrape_page(cached=False)` — fetches live or reads from cache; prints each product inline; returns `(products, parsed_count, total_cards)`
- `main()` — parses `--cached` flag, calls `scrape_page()`, writes result file, prints summary

### scrape-dshome.py

- `scrape_page(page, cached=False)` — reads `dshome/page-{page}.html` or fetches. Uses `a[href*='/boltove/']` for cards, `h3` for name, `span.text-red-600` for price (the site pre-formats both EUR and BGN into this span).
- `main()` — loops pages 1–24, writes `result-dshome.txt`, sleeps 0.5s between live requests (skipped when cached).

### scrape-praktiker.py

- Uses `te-product-box` for cards, first long `<a>` for name, `.price-wrapper` spans for EUR/BGN.
- Writes `result-praktiker.txt`.

### scrape-mrbricolage.py

- Uses `div.product` for cards, `h2.product__title a` for name, `div.product__price-value` for EUR/BGN.
- Writes `result-mrbricolage.txt`.

### scrape-bauhaus.py

- Uses `div.product_holder` for cards, `a.product-name` for name, `div.product-price table tr` rows for EUR/BGN (price split across `td`/`sup` elements).
- Writes `result-bauhaus.txt`.

### scrape-homemax.py

- Uses `div.product-box-item` for cards, `.product-box-title` for name, `.price-item-wrapper` for EUR/BGN (price split across `.price-holder` text + `sup` for decimals, `.currency` for unit).
- Writes `result-homemax.txt`.

## Known limitations / TODOs

- Page count (24) for dshome is hardcoded; dynamic detection not implemented.
- All URLs are hardcoded to specific categories.
