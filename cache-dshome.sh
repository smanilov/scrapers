#!/usr/bin/env bash
set -eo pipefail

mkdir -p dshome

for page in $(seq 1 24); do
    echo "Downloading page $page..."
    curl -A "Mozilla/5.0 (X11; Linux x86_64)" -o "dshome/page-${page}.html" \
        "https://www.dshome.bg/boltove?page=${page}"
    sleep 0.5
done
