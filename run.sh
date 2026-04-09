#!/usr/bin/env bash
set -eo pipefail

script="${1:?Usage: run.sh <dshome|praktiker|mrbricolage> [--cached]}"
shift

python3 "scrape-${script}.py" "$@"
