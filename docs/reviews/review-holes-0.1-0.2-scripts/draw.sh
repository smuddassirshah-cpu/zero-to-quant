#!/bin/sh
# Draws 20 items of every family of the nine level 4 Fluency sets into <out>/<course>__<set>__<family>.json
# sh docs/reviews/review-holes-0.1-0.2-scripts/draw.sh <out dir>      (from the repo root)
out="$1"
mkdir -p "$out"
for s in number-sense/fluency-l15-building-blocks number-sense/fluency-l16-shared-factors number-sense/fluency-l17-around-and-inside \
         number-sense/fluency-l18-circles-and-units number-sense/fluency-l19-one-number-for-many quadratics/fluency-l14-roots-that-stay \
         quadratics/fluency-l15-fractions-with-letters quadratics/fluency-l16-adding-and-solving quadratics/fluency-l17-dividing-polynomials; do
  fams=$(python3 -c "import json,sys; print(' '.join(f['id'] for f in json.load(open('app/content/courses/'+sys.argv[1]+'.json'))['families']))" "$s")
  for f in $fams; do
    node app/tools/fluency-sample.mjs --set "$s" --family "$f" --seed 7001 --n 20 --json > "$out/$(echo "$s" | tr '/' '_')__$f.json" || echo "DRAW FAILED $s $f"
  done
done
ls "$out" | wc -l
