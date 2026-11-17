# Exam second item: topics 2.1, 2.3, 2.6 and 3.2 (NAME 2.x-3.2)

Brief: `docs/briefs/exam-second-item.md`, Author section. Numbers: `docs/reports/exam-second-item-2.x-3.2-numbers.py` (exit 0). Scratch: `SCRATCH/exam2-2.x-3.2/` (`pairs.py` recomputes the pairs, `items.py` and `build.py` splice the items, keeping each file's formatting).

## Pairs, recomputed

Rule: for each level of every `course.json` in the topic, the essential skills are the skills on its review's items; a pair is an exam skill with at most one auto (non-longform) item. Recomputed from the files on disk (`ito`, `measure-prob` and `pdes` reviews all present; their problem sets are not needed). Same as the 16 Nov table: 9 triples, 6 pairs.

| exam | levels | skill | auto items before | after |
|---|---|---|---|---|
| topic-3.2 | pdes/L3 | pe-bs | 1 (e-heat-change) | 2 |
| topic-3.2 | pdes/L3 | pe-fk | 1 (e-fk-square) | 2 |
| topic-3.2 | pdes/L3 | pe-fd | 1 (e-explicit-code) | 2 |
| topic-2.1 | ensembles/L1, L2, L3 | en-interpret | 1 (e-importance-claims) | 2 |
| topic-2.3 | backtest/L4 | bt-report | 1 (e-too-good; e-results-note is longform) | 2 |
| topic-2.6 | stat-models/L4 | sm-hier | 1 (e-hit-rate-shrink) | 2 |

Pairs left: none.

## New items

| exam | id | skills | d | widget | task |
|---|---|---|---|---|---|
| topic-3.2 | e-heat-grid-steps | pe-bs, pe-fd | 3 | numeric (46) | fewest explicit steps: heat time $\tfrac12\sigma^2T$ (pe-bs) against $\lambda \le \tfrac12$ (pe-fd); neither alone gives it |
| topic-3.2 | e-fk-reverting | pe-fk | 3 | numeric (1.7561) | read a mean-reverting process off its PDE, then $e^{-rT}E[X_T]$ for a linear payoff |
| topic-2.1 | e-pd-two-trees | en-interpret | 3 | numeric, console canvas (1.5 bp) | partial dependence by hand on a two-tree forest; the conditional-means slip gives 4.0 |
| topic-2.3 | e-honest-bar | bt-report | 3 | parts: numeric (0.88) and choice | honest count of settings (36 dropped + 24) and the no-edge bar, then the note's line |
| topic-2.6 | e-two-fund-shrink | sm-hier | 4 | parts: two numeric, unit % (1.8%, 3.94%) | normal-normal shrinkage with each fund's own $B_j$ |

Rule (b) used once (e-heat-grid-steps carries pe-bs and pe-fd), so topic 3.2 needed two swaps, not three.

## Removed items (rule c)

| exam | removed id | d | skills | auto items left on each skill |
|---|---|---|---|---|
| topic-3.2 | e-drift-t2w2 | 3 | it-calculus | it-calculus 4 (most covered skill; its Itô-drift task repeats e-pick-martingales and e-sixth-repair) |
| topic-3.2 | e-gbm-below | 3 | it-bm | it-bm 3 |
| topic-2.1 | e-odds-update | 3 | sl-classify | sl-classify 5 (the most covered skill) |
| topic-2.3 | e-impact-double | 3 | bt-execution | bt-execution 4 (the most covered skill) |

Each swap replaces a difficulty 3 item with a difficulty 3 item, so the mix of topics 2.1, 2.3 and 3.2 is unchanged. Topic 2.6 gains a difficulty 4 item (rule a: 25 items, now 26; d2 5, d3 13, d4 6, d5 2). After the changes every skill of the four exams has at least two auto items (lowest: 2).

## Minutes

Topics 2.1, 2.3 and 3.2 keep 30 items and 90 minutes. Topic 2.6: 75 × 26/25 = 78, rounded to 80 minutes (+5 min, 0.08 h); the main session runs `readiness-sums.mjs --write`.

## Reuse

`fresh-check.mjs --file` on each exam: 0 hits; no advisory on any new item after one rewording (the bt-report question first shared the stem "what is the expected best under no edge" with `l15` screen 4, `review-4` and `homework-4`). Number sets are new against the courses and exams: σ 35%, T 0.6, Δx 0.04 (e-heat-change uses σ 25%, T 0.75; l12 and homework-3 use Δx 0.02 and 0.05); κ 0.3, level 3, r 4% (l11's Vasicek uses κ 0.5); the forest trees and rows; 36 + 24 settings with sd 0.38 (l15: 48, 72 + 48, sd 0.40, 0.451, 0.345); μ 1%, τ 2%, funds 9%/6% and 5%/1.2% (l18: μ 2.2478, τ 1.6943; e-alpha-prior: 8%/3%, prior sd 1.5).

## Gates

- `node tools/validate.mjs`: 0 errors; no warning on any new item.
- `VOICE_BASE=app/content/exams python3 docs/reviews/voice-scan.py 35`: 0 and 0.
- `grade-all.mjs --file` with `--local-cdn`: 0 failures on each of the four exams.
- `playthrough.mjs --exam <id> --local-cdn`: topic-3.2, 2.1, 2.3, 2.6 all passed, desktop and `--mobile`. Screenshots of the five new items at 440 px read: the console's arrows in e-pd-two-trees were realigned after the first look; nothing else to fix.
- Numbers script: every key, `wrong` value and printed figure, most two ways (formula and stepped ODE; partial dependence at two pairs of values; expected maxima by integration and simulation; shrinkage as $\mu + (1 - B)(\hat\alpha - \mu)$ and as a precision-weighted mean). Exit 0.

## Engine limits

None found.
