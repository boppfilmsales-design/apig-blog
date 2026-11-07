#!/usr/bin/env bash
# Assemble a publish-ready copy of the site for Cloudflare Pages.
#
# The repository keeps its Python pipeline under build/ and a few helper
# scripts at the root. Those are source material, not site content, so a Git
# build must copy only the runtime files into the output directory instead of
# deploying the working tree wholesale.
set -euo pipefail

OUT="${1:-dist}"

rm -rf "$OUT"
mkdir -p "$OUT"

cp index.html "$OUT/"
cp _redirects "$OUT/"
cp -r en zh assets "$OUT/"

# Cloudflare Pages serves the root 404.html for unmatched paths. Without it
# every unknown URL answers 200 with the homepage, which search engines
# treat as duplicate content.
if [ -f 404.html ]; then
  cp 404.html "$OUT/"
fi

# Guard against publishing an empty or partial site.
for required in index.html _redirects en/index.html zh/index.html assets/css/site.css assets/js/site.js; do
  if [ ! -f "$OUT/$required" ]; then
    echo "build_pages.sh: missing required file $required" >&2
    exit 1
  fi
done

echo "build_pages.sh: assembled $(find "$OUT" -type f | wc -l) files into $OUT/"
