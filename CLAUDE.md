# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this project does

Scrapes product listings (names and prices) from eight sites:

- `dshome.bg/boltove` — bolts/fasteners, 24 pages, output to `results/dshome.txt`
- `praktiker.bg` — compressors, single page, output to `results/praktiker.txt`
- `mr-bricolage.bg` — compressors, single page, output to `results/mrbricolage.txt`
- `bauhaus.bg` — compressors/pumps, single page, output to `results/bauhaus.txt`
- `home-max.bg` — compressors/pumps, single page, output to `results/homemax.txt`
- `temax.bg` — compressors, single page, output to `results/temax.txt`
- `masterhaus.bg` — compressors, single page, output to `results/masterhaus.txt`
- `praktis.bg` — compressors, single page, output to `results/praktis.txt`

## Running the scrapers

`run.sh` is the canonical entry point:

```bash
./run.sh <dshome|praktiker|mrbricolage|bauhaus|homemax|temax|masterhaus|praktis> [--cached]
```

Or directly (run from the project root):

```bash
python3 scrapers/dshome.py [--cached]
python3 scrapers/praktiker.py [--cached]
# etc.
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
./cache.sh <dshome|praktiker|mrbricolage|bauhaus|homemax|temax|masterhaus|praktis>
```

Saves to `cache/`. All targets use `-L` (follow redirects) and a Firefox user-agent. mr-bricolage additionally sends `Accept`/`Accept-Language` headers required for SSR rendering.

Then run with `--cached` to parse from disk.

## Dependencies

- `requests`
- `beautifulsoup4`

Install with: `pip install requests beautifulsoup4`

## Code structure

### common.py

Shared infrastructure used by all scrapers except dshome:

- `HEADERS` — default Firefox user-agent dict
- `load_html(url, cache_file, headers, cached)` — fetches live or reads from cache file
- `scrape(url, cache_file, headers, cached, get_cards, get_name, get_price)` — shared iteration loop: parse HTML, call `get_cards(soup)` for the list of card elements, then call `get_name(box)` and `get_price(box)` per card; skips cards where either returns `None`; prints inline and returns `(products, parsed_count, total_cards)`
- `write_results(result_file, products, parsed_count, total_cards)` — writes output file
- `run(result_file, cache_file, scrape_fn)` — parses `--cached` flag, calls `scrape_fn`, writes results, prints summary

### dshome.py

Standalone (does not use common.py). Loops pages 1–24, sleeps 0.5s between live requests.

### Single-page scrapers (praktiker, mrbricolage, bauhaus, homemax, temax, masterhaus, praktis)

Each defines `get_cards(soup)`, `get_name(box)`, `get_price(box)` and delegates to `common`. Non-obvious details:

- **mrbricolage** — requires extra `Accept`/`Accept-Language` headers for SSR rendering; defined locally instead of using the shared `HEADERS`
- **masterhaus** — `_parse_price()` reconstructs price from split DOM: direct text + `<sup>` decimal + `<abbr>` currency
- **praktis** — each product card appears 4× in the HTML; `get_cards()` deduplicates by product ID from `data-name`

## Testing

`test.sh` runs every scraper with `--cached` and checks that `results/*.txt` is unchanged:

```bash
./test.sh
```

Uses `git diff` (working tree vs index) to detect changes. All result files are tracked, so any output regression shows up as a diff. `__pycache__/` is gitignored and safe to leave in place.

## Known limitations / TODOs

- Page count (24) for dshome is hardcoded.
- All URLs are hardcoded to specific categories.
