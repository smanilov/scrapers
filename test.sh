#!/usr/bin/env bash
set -eo pipefail

GREEN='\033[0;32m'
RED='\033[0;31m'
BOLD='\033[1m'
RESET='\033[0m'

PASS=0
FAIL=0

for name in bauhaus dshome homemax masterhaus mrbean2cup mrbricolage praktiker praktis temax; do
    printf "%-14s" "$name"
    python3 "scrapers/${name}.py" --cached > /dev/null
    if git diff --stat -- "results/${name}.txt" | grep -q "results/"; then
        printf "${RED}FAIL (output changed)${RESET}\n"
        git diff --stat -- "results/${name}.txt"
        FAIL=$((FAIL + 1))
    else
        printf "${GREEN}ok${RESET}\n"
        PASS=$((PASS + 1))
    fi
done

echo ""
printf "${BOLD}$PASS passed, $FAIL failed${RESET}\n"
[ "$FAIL" -eq 0 ]
