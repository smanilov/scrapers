#!/usr/bin/env bash
set -eo pipefail

target="${1:?Usage: cache.sh <dshome|praktiker|mrbricolage|bauhaus|homemax|temax|masterhaus|praktis|autodoc|mrbean2cup>}"

python3 "scrapers/${target}.py" --download
