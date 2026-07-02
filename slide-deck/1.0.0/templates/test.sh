#!/usr/bin/env bash
# Smoke test for the slide-deck skill templates.
# Scaffolds a temp deck, runs `make`, asserts all three PDFs build non-empty.
# Run once after installing the skill, before first real use.

set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TMP="$(mktemp -d -t slide-deck-test.XXXXXX)"
trap 'rm -rf "$TMP"' EXIT

echo "Scaffolding into $TMP ..."
cp -r "$HERE"/* "$TMP/"
mv "$TMP/slides.md.template" "$TMP/slides.md"
# Strip handlebars so pandoc can parse the YAML header.
sed -i 's/{{TITLE}}/Test deck/;        s/{{SUBTITLE}}/smoke/;
        s/{{AUTHOR}}/Test/;            s/{{DATE}}/today/' "$TMP/slides.md"

cd "$TMP"
echo "Building slides.pdf ..."
make slides.pdf
echo "Building notes.pdf ..."
make notes.pdf
echo "Building slides-pdfpc.pdf ..."
make slides-pdfpc.pdf

fail=0
for f in slides.pdf notes.pdf slides-pdfpc.pdf; do
  if [[ ! -s "$f" ]]; then
    echo "FAIL: $f is missing or empty" >&2
    fail=1
  else
    echo "OK:   $f ($(stat -c %s "$f") bytes)"
  fi
done
exit "$fail"
