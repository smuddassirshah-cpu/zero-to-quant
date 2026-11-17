# Exam second item, topic 1.5 (session AG)

File: `app/content/exams/topic-1.5.json`. Was 30 items, 60 minutes; now 35 items, 70 minutes (60 x 35 / 30 = 70). Hours note: the exam grows by 10 minutes; the main session runs `readiness-sums.mjs --write`.
Generator: `scratchpad/exam2-1.5/gen.py`. Numbers: `docs/reports/exam-second-item-1.5-numbers.py` (74 checks, exit 0).

## Pairs (recomputed)

Rule: essential skills of a level are the skills on its `review-<n>` items; an (exam, skill) pair is listed when the exam holds exactly one non-longform item on it. Over the five topic-1.5 courses: 12 pairs, 25 triples, the same as the 16 Nov table.

| skill | levels |
|---|---|
| cc-sample | counting-chance L1, L2 |
| cc-count | counting-chance L1, L2, L3 |
| cc-rules | counting-chance L1, L2, L3 |
| cc-symmetry | counting-chance L1, L3 |
| cond-shrink | conditional L1 |
| cond-mult | conditional L1, L3, L5 |
| bayes | conditional L2, L5 |
| rv-dist | random-vars L1 |
| dl-lln | limits-thm L3 |
| dl-clt | limits-thm L3 |
| mc-firststep | markov L2, L3, L5 |
| mc-walks | markov L3, L4, L5 |

## New items (7)

| id | d | skills | widget | why both skills (option b) |
|---|---|---|---|---|
| e-ticket-pair | 2 | cc-sample, cc-count | numeric | list the 10 unordered pairs, count the even-sum ones |
| e-neither-market | 3 | cc-rules, cc-symmetry | numeric | inclusion and exclusion, then the complement |
| e-multiple-four | 2 | cond-shrink | choice | |
| e-coin-again | 3 | bayes, cond-mult | numeric | posterior after one head, then total probability over the coins |
| e-distance-three | 2 | rv-dist | choice | |
| e-fill-times | 3 | dl-lln, dl-clt | table | (a) Chebyshev on the mean, (b) CLT on the same event |
| e-floor-walk | 4 | mc-walks, mc-firststep | numeric, markov graph | a walk with a reflecting floor: the ruin formula does not apply, first-step equations do |

Option (b) placed 10 skills in 5 items; cond-shrink and rv-dist stand alone (no honest partner among the pairs).

## Removed (option c, 2)

| id | d | skills | skill keeps |
|---|---|---|---|
| e-wait-six | 2 | dl-discrete | e-winning-days, e-order-split |
| e-uniform | 3 | dl-continuous | e-beta-pair, e-default-pair |

Not removed, though counts allowed: `e-two-days` (mc-chains). It is the only item on multi-step transitions; mc-chains would then rest on a Metropolis item and a Poisson-splitting item, which leaves markov L1 with no basic test. So 35 items, not 34.

## Checks

- Every listed pair now has two auto items; no skill of the exam is below two (script checks both).
- Difficulty 7 / 16 / 9 / 3 (20 / 46 / 26 / 9%), against the old 5 / 14 / 8 / 3.
- Reuse: `fresh-check.mjs --file` 0 hits; one advisory on `e-ticket-pair` (stem run shared with `mock-oa-trader-3`) was reworded away. The other 13 advisories are on old items. Greps for 89/130, 2/7, 2.5^2 and the floor walk equations find no shared task.
- Bands: every `wrong` value lies outside the key band and no wrong band holds the key; no key on a rounding tie; Φ(2.5) is printed in the prose.
- Gates: validator 0 errors; voice scan 0 and 0; `grade-all --file` 35 widgets, 0 failures; playthrough green with and without `--mobile`. Screenshot check: the 440 px graph is small but legible (inbox bullet).

Pairs left: none.
