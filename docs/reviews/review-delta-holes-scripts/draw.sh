#!/bin/sh
# Draws n items (default 200) of each Fluency family the two fix passes changed into <out>/<family>.json
# sh docs/reviews/review-delta-holes-scripts/draw.sh <out dir> [seed] [n]     (from the repo root)
out="$1"; seed="${2:-4711}"; n="${3:-200}"
mkdir -p "$out"
while read -r set fam; do
  node app/tools/fluency-sample.mjs --set "$set" --family "$fam" --seed "$seed" --n "$n" --json > "$out/$fam.json" || echo "DRAW FAILED $set $fam"
done <<'L'
testing/fluency-l18-counts-against-expectations two-by-two
testing/fluency-l17-ratio-of-likelihoods poisson-ratio-test
testing/fluency-l17-ratio-of-likelihoods wilks-df
testing/fluency-l15-sharpness-of-the-peak volatility-se
stat-learning/fluency-l16-groups-nobody-labelled assign-and-update
stat-learning/fluency-l16-groups-nobody-labelled linkage-distance
stat-learning/fluency-l18-bending-the-line slope-in-a-region
quadratics/fluency-l16-adding-and-solving add-tops
quadratics/fluency-l16-adding-and-solving subtract-tops
quadratics/fluency-l17-dividing-polynomials quotient
quadratics/fluency-l14-roots-that-stay conjugate-bottom
number-sense/fluency-l16-shared-factors other-number
number-sense/fluency-l15-building-blocks count-factors
number-sense/fluency-l19-one-number-for-many table-mean
L
ls "$out" | wc -l
