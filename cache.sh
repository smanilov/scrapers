#!/usr/bin/env bash
set -eo pipefail

target="${1:?Usage: cache.sh <dshome|praktiker|mrbricolage>}"

UA="Mozilla/5.0 (X11; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0"

case "$target" in
    dshome)
        mkdir -p dshome
        for page in $(seq 1 24); do
            echo "Downloading page $page..."
            curl -L -A "$UA" -o "dshome/page-${page}.html" \
                "https://www.dshome.bg/boltove?page=${page}"
            sleep 0.5
        done
        ;;
    praktiker)
        curl -L -A "$UA" -o praktiker_cache.html \
            "https://praktiker.bg/en/Avto-i-velo/Sigurnost-i-bezopasnost/Kompresori/c/P13060305?pageSize=92&currentPage=0"
        ;;
    mrbricolage)
        curl -L -A "$UA" \
            -H "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" \
            -H "Accept-Language: bg,en;q=0.5" \
            -o mrbricolage_cache.html \
            "https://mr-bricolage.bg/instrumenti/avtoaksesoari/kompresori-pompi/c/006008021?pageSize=50"
        ;;
    *)
        echo "Unknown target: $target" >&2
        exit 1
        ;;
esac
