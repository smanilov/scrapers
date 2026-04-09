# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this project does

Scrapes bolt/fastener product listings (names and prices) from `dshome.bg/boltove`, paginating through 24 pages, and saves the output to `result.txt`.

## Running the scraper

See `run.sh` for the canonical invocation. Directly:

```bash
python3 scrape.py
```

Output is written to `result.txt` in the format:
```
=== PAGE N ===
Parsed: X / Y
Product name | price
```

## Dependencies

- `requests`
- `beautifulsoup4`

Install with: `pip install requests beautifulsoup4`

## Code structure

All logic is in `scrape.py`:

- `scrape_page(page)` — fetches and parses one page; returns `(products, parsed_count, total_cards)`. Uses CSS selector `a[href*='/boltove/']` to find product cards, then `h3` for name and `span.text-red-600` for price.
- `main()` — loops pages 1–24, writes results to `result.txt`, sleeps 0.5s between requests.

## Known limitations / TODOs (from git history)

- Page count (24) is hardcoded; dynamic detection of total pages is not yet implemented.
- Results-per-page is fixed at 24; was noted as needing attention.
- Caching was added but there is no cache invalidation or conditional fetch logic visible in current code.
