#!/usr/bin/env bash
set -eo pipefail

script="${1:?Usage: run.sh <dshome|praktiker|mrbricolage|bauhaus|homemax|temax|masterhaus|praktis|autodoc|mrbean2cup> [--cached]}"
shift

python3 "scrapers/${script}.py" "$@"
