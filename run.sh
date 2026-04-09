#!/usr/bin/env bash
set -eo pipefail

script="${1:?Usage: run.sh <dshome|praktiker|mrbricolage|bauhaus|homemax|temax|masterhaus|praktis> [--cached]}"
shift

python3 "scrape-${script}.py" "$@"
