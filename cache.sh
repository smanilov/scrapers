#!/usr/bin/env bash
set -eo pipefail

target="${1:?Usage: cache.sh <dshome|praktiker>}"

case "$target" in
    dshome)
        mkdir -p dshome
        for page in $(seq 1 24); do
            echo "Downloading page $page..."
            curl -A "Mozilla/5.0 (X11; Linux x86_64)" -o "dshome/page-${page}.html" \
                "https://www.dshome.bg/boltove?page=${page}"
            sleep 0.5
        done
        ;;
    praktiker)
        curl -A "Mozilla/5.0 (X11; Linux x86_64)" -o praktiker_cache.html \
            "https://praktiker.bg/en/Avto-i-velo/Sigurnost-i-bezopasnost/Kompresori/c/P13060305?pageSize=92&currentPage=0"
        ;;
    *)
        echo "Unknown target: $target" >&2
        exit 1
        ;;
esac
