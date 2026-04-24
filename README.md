# scrapers

Scrapes product listings (names and prices) from home improvement and automotive stores.

## Sites

| Site | Category | Pages | Output |
|---|---|---|---|
| dshome.bg | Bolts/fasteners | 24 | `results/dshome.txt` |
| praktiker.bg | Compressors | 1 | `results/praktiker.txt` |
| mr-bricolage.bg | Compressors | 1 | `results/mrbricolage.txt` |
| bauhaus.bg | Compressors/pumps | 1 | `results/bauhaus.txt` |
| home-max.bg | Compressors/pumps | 1 | `results/homemax.txt` |
| temax.bg | Compressors | 1 | `results/temax.txt` |
| masterhaus.bg | Compressors | 1 | `results/masterhaus.txt` |
| praktis.bg | Compressors | 1 | `results/praktis.txt` |
| autodoc.parts | Car jacks | 42 | `results/autodoc.txt` |

## Usage

```bash
./run.sh <target> [--cached]
```

Where `<target>` is one of: `dshome`, `praktiker`, `mrbricolage`, `bauhaus`, `homemax`, `temax`, `masterhaus`, `praktis`, `autodoc`.

Pass `--cached` to parse from a previously downloaded local copy instead of making live requests.

## Output format

```
=== PRODUCTS ===
Parsed: 18 / 18
Air compressor 50L | 189.99 € | 371.56 лв.
...
```

The Bulgarian store scrapers report prices in both EUR and BGN. The autodoc scraper reports EUR only, one entry per page:

```
=== PAGE 1 ===
Parsed: 20 / 20
YATO YT-17211 Jack3t, Hydraulic, SUVs, Trolley jack | 107, 49 €
...
```

autodoc also handles 403 responses with automatic retry and exponential backoff.

## Caching

Download pages locally before running offline:

```bash
./cache.sh <target>
```

Saves HTML to `cache/`. Useful for repeated runs without hammering the sites.

## Testing

```bash
./test.sh
```

Runs all scrapers (apart from autodoc) with `--cached` and uses `git diff` to detect any output regressions.

## Dependencies

```bash
pip install requests beautifulsoup4
```
