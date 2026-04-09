# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this project does

Scrapes product listings (names and prices) from eight sites:

- `dshome.bg/boltove` — bolts/fasteners, 24 pages, output to `result-dshome.txt`
- `praktiker.bg` — compressors, single page, output to `result-praktiker.txt`
- `mr-bricolage.bg` — compressors, single page, output to `result-mrbricolage.txt`
- `bauhaus.bg` — compressors/pumps, single page, output to `result-bauhaus.txt`
- `home-max.bg` — compressors/pumps, single page, output to `result-homemax.txt`
- `temax.bg` — compressors, single page, output to `result-temax.txt`
- `masterhaus.bg` — compressors, single page, output to `result-masterhaus.txt`
- `praktis.bg` — compressors, single page, output to `result-praktis.txt`

## Running the scrapers

`run.sh` is the canonical entry point:

```bash
./run.sh <dshome|praktiker|mrbricolage|bauhaus|homemax|temax|masterhaus|praktis> [--cached]
```

Or directly (run from the project root):

```bash
python3 scrapers/scrape-dshome.py [--cached]
python3 scrapers/scrape-praktiker.py [--cached]
python3 scrapers/scrape-mrbricolage.py [--cached]
python3 scrapers/scrape-bauhaus.py [--cached]
python3 scrapers/scrape-homemax.py [--cached]
python3 scrapers/scrape-temax.py [--cached]
python3 scrapers/scrape-masterhaus.py [--cached]
python3 scrapers/scrape-praktis.py [--cached]
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
./cache.sh dshome       # saves cache/dshome/page-1.html … page-24.html
./cache.sh praktiker    # saves cache/praktiker_cache.html
./cache.sh mrbricolage  # saves cache/mrbricolage_cache.html
./cache.sh bauhaus      # saves cache/bauhaus_cache.html
./cache.sh homemax      # saves cache/homemax_cache.html
./cache.sh temax        # saves cache/temax_cache.html
./cache.sh masterhaus   # saves cache/masterhaus_cache.html
./cache.sh praktis      # saves cache/praktis_cache.html
```

All targets use `-L` (follow redirects) and a realistic Firefox user-agent. mr-bricolage additionally sends `Accept` and `Accept-Language` headers required for SSR rendering.

Then run with `--cached` to parse from disk.

## Dependencies

- `requests`
- `beautifulsoup4`

Install with: `pip install requests beautifulsoup4`

## Code structure

### scrape_common.py

Shared infrastructure used by all scrapers except dshome:

- `HEADERS` — default Firefox user-agent dict
- `load_html(url, cache_file, headers, cached)` — fetches live or reads from cache file
- `scrape(url, cache_file, headers, cached, get_cards, get_name, get_price)` — shared iteration loop: parse HTML, call `get_cards(soup)` for the list of card elements, then call `get_name(box)` and `get_price(box)` per card; skips cards where either returns `None`; prints inline and returns `(products, parsed_count, total_cards)`
- `write_results(result_file, products, parsed_count, total_cards)` — writes output file
- `run(result_file, cache_file, scrape_fn)` — parses `--cached` flag, calls `scrape_fn`, writes results, prints summary

### scrape-dshome.py

- `scrape_page(page, cached=False)` — reads `cache/dshome/page-{page}.html` or fetches. Uses `a[href*='/boltove/']` for cards, `h3` for name, `span.text-red-600` for price (the site pre-formats both EUR and BGN into this span).
- `main()` — loops pages 1–24, writes `result-dshome.txt`, sleeps 0.5s between live requests (skipped when cached).

### Single-page scrapers (praktiker, mrbricolage, bauhaus, homemax, temax, masterhaus, praktis)

Each defines `get_cards(soup)`, `get_name(box)`, `get_price(box)` and delegates to `scrape_common.scrape()` and `scrape_common.run()`. Site-specific notes:

- **praktiker** — `te-product-box` cards; first long `<a>` for name; `.price-wrapper` spans for EUR/BGN
- **mrbricolage** — `div.product` cards; `h2.product__title a` for name; `div.product__price-value` for EUR/BGN; extra `Accept`/`Accept-Language` headers required for SSR rendering
- **bauhaus** — `div.product_holder` cards; `a.product-name`; price from `div.product-price table tr` (value split across `td`/`sup`, currency in `small`)
- **homemax** — `div.product-box-item` cards; `.product-box-title`; price from `.price-item-wrapper` (`.price-holder` text + `sup` decimal, `.currency` unit)
- **temax** — `li.product-item` cards; `a.product-item-link`; `span.price` for EUR, `span.side-price` direct text nodes for BGN
- **masterhaus** — `li[data-id]` cards; `h2 a`; `_parse_price()` helper reconstructs price from direct text + `sup` decimal + `abbr` currency (e.g. `96` + `63` + `€` → `96.63 €`)
- **praktis** — `article[data-name^="pc:root:"]` cards, deduplicated by product ID (each appears 4× in HTML); `a[data-name^="pc:default-title:"] span` for name; prices from `span[data-name="price-info-regular-price-*"]` elements

## Known limitations / TODOs

- Page count (24) for dshome is hardcoded; dynamic detection not implemented.
- All URLs are hardcoded to specific categories.
