#!/usr/bin/env bash
set -eo pipefail

target="${1:?Usage: cache.sh <dshome|praktiker|mrbricolage|bauhaus|homemax|temax|masterhaus|praktis|autodoc>}"

UA="Mozilla/5.0 (X11; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0"

case "$target" in
    dshome)
        mkdir -p cache/dshome
        for page in $(seq 1 24); do
            echo "Downloading page $page..."
            curl -L -A "$UA" -o "cache/dshome/page-${page}.html" \
                "https://www.dshome.bg/boltove?page=${page}"
            sleep 0.5
        done
        ;;
    praktiker)
        curl -L -A "$UA" -o cache/praktiker.html \
            "https://praktiker.bg/en/Avto-i-velo/Sigurnost-i-bezopasnost/Kompresori/c/P13060305?pageSize=92&currentPage=0"
        ;;
    mrbricolage)
        curl -L -A "$UA" \
            -H "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" \
            -H "Accept-Language: bg,en;q=0.5" \
            -o cache/mrbricolage.html \
            "https://mr-bricolage.bg/instrumenti/avtoaksesoari/kompresori-pompi/c/006008021?pageSize=50"
        ;;
    bauhaus)
        curl -L -A "$UA" -o cache/bauhaus.html \
            "https://bauhaus.bg/pompi-i-kompresori-za-gumi/c/1928"
        ;;
    homemax)
        curl -L -A "$UA" -o cache/homemax.html \
            "https://www.home-max.bg/instrumenti-i-oborudvane/avtoprinadlejnosti/avtoinstrumenti/pompi-i-kompresori/"
        ;;
    temax)
        curl -L -A "$UA" -o cache/temax.html \
            "https://temax.bg/avto-i-velo-aksesoari/avtomobilni-prinadlezhnosti/PRODUCTAVTO-kompresor"
        ;;
    masterhaus)
        curl -L -A "$UA" -o cache/masterhaus.html \
            "https://www.masterhaus.bg/bg/products/mashini-i-instrumenti/stroitelna-tehnika-i-mashini/kompresori"
        ;;
    praktis)
        curl -L -A "$UA" -o cache/praktis.html \
            "https://praktis.bg/avto-i-velo-svyat/preporachitelno-oborudvane-za-avtomobil/kompresori-za-avtomobil"
        ;;
    autodoc)
        mkdir -p cache/autodoc
        for page in $(seq 1 28); do
            echo "Downloading page $page..."
            curl -L -A "$UA" -o "cache/autodoc/page-${page}.html" \
                "https://www.autodoc.parts/car-accessories/car-jacks?all-categories=all&categories%5B0%5D=4710%7C5203&page=${page}"
            sleep 0.5
        done
        ;;
    *)
        echo "Unknown target: $target" >&2
        exit 1
        ;;
esac
