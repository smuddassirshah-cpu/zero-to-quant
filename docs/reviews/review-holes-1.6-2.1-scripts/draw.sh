#!/bin/sh
# Draws 20 items of every family of the eight level 4 Fluency sets into <out>/<course>_<set>__<family>.json
# sh docs/reviews/review-holes-1.6-2.1-scripts/draw.sh <out dir> [seed] [n]     (from the repo root)
out="$1"
seed="${2:-8101}"
n="${3:-20}"
mkdir -p "$out"
for s in testing/fluency-l13-matching-moments testing/fluency-l15-sharpness-of-the-peak testing/fluency-l17-ratio-of-likelihoods \
         testing/fluency-l18-counts-against-expectations stat-learning/fluency-l15-widest-street stat-learning/fluency-l16-groups-nobody-labelled \
         stat-learning/fluency-l17-a-small-network stat-learning/fluency-l18-bending-the-line; do
  fams=$(python3 -c "import json,sys; print(' '.join(f['id'] for f in json.load(open('app/content/courses/'+sys.argv[1]+'.json'))['families']))" "$s")
  for f in $fams; do
    node app/tools/fluency-sample.mjs --set "$s" --family "$f" --seed "$seed" --n "$n" --json > "$out/$(echo "$s" | tr '/' '_')__$f.json" || echo "DRAW FAILED $s $f"
  done
done
ls "$out" | wc -l
