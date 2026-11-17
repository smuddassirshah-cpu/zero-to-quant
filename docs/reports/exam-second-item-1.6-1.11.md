# Second auto item for one-item exam skills: topics 1.6 to 1.11

Brief: `docs/briefs/exam-second-item.md`. Scratch: `scratchpad/exam2-1.6-1.11/` (`pairs.py` recomputes the pairs, `gen.py` writes the items).
Numbers: `docs/reports/exam-second-item-1.6-1.11-numbers.py`, 174 of 174 checks after the fix pass (s-three-traders and e-just-paid retargeted, e-swapped-d printed values), exit 0.

## Pairs, recomputed

Rule: for each `course.json` of the topic, each level with a review, the review's item skills are the essentials; a pair is an essential skill with at most one auto (non-longform) item in the topic exam. Recomputed from the files today; it matches the 16 Nov table (none with zero items).

| exam | pairs (level) |
|---|---|
| topic-1.6 | es-bayes (estimation/L3) |
| topic-1.7 | op-payoff (options/L1), op-strategies (options/L1, L2, L3), fi-bonds, fi-equity (markets/L2), tp-replicate (trees/L1) |
| topic-1.8 | gd-backtrack (graphs-dp/L3) |
| topic-1.9 | cx-testing (cpp-pricing/L1, L2, L3) |
| topic-1.10 | lx-dual (linear-maps/L3) |
| topic-1.11 | cz-arith (complex/L1) |

## New items

| exam | id | skills | d | widget | rule | removed (skills) |
|---|---|---|---|---|---|---|
| topic-1.6 | s-three-traders (re-storied after the second read: sellers, Beta(27, 3), on-time orders) | es-bayes | 3 | choice | (a) after the fix pass | none (s-alpha-beta-table restored at its old position; exam holds 31 items, minutes 70) |
| topic-1.7 | e-ratio-spread | op-strategies, op-payoff | 3 | parts: numeric, numeric, payoff canvas | (b)+(c) | e-book-delta (op-greeks; 5 to 4) |
| topic-1.7 | e-capped-copy | tp-replicate | 2 | choice, tree graph | (c) | e-one-step-q (tp-riskneutral; 6 to 5) |
| topic-1.7 | e-zero-yield | fi-bonds | 3 | parts: numeric %, numeric | (c) | e-parity-put (op-parity; 5 to 4) |
| topic-1.7 | e-just-paid (numbers changed in the fix pass: £3.20, 5%, 9%, key £84.00) | fi-equity | 3 | numeric | (c) | e-short-sale (fi-forwards; 4 to 3) |
| topic-1.8 | e-venue-split | gd-backtrack | 4 | parts: choice, numeric, graph | (a) | none |
| topic-1.9 | e-swapped-d | cx-testing | 4 | multi (C++ tests) | (c) | e-virtual-dtor (cp-classes; 6 to 5) |
| topic-1.10 | e-integral-weights | lx-dual | 3 | table | (c) | e-cube-delta (an-continuity; 4 to 3) |
| topic-1.11 | e-square-root-parts | cz-arith | 3 | expression, form rectangular | (c) | e-integrating-factor (de-first; 3 to 2) |

Each swap takes the place and difficulty of the removed item, so every difficulty mix is unchanged; topic 1.8 gains a 4 (now 6, 14, 6, 3 of 29). Removed items were the most duplicated: e-book-delta beside e-copy-short-calls (both short-call hedges), e-one-step-q beside the one-step trees, e-parity-put among four parity items, e-virtual-dtor beside the polymorphic e-code-clone-basket. In e-ratio-spread each leg's payoff (op-payoff) and the sum of legs with the net premium (op-strategies) are both needed. Pairs left: none. After the change every skill of all six exams has at least two auto items (`pairs.py`).

Reuse: each item is a new task on its skill (ranking by posterior, ratio spread, a capped-note copy, yield from a zero's price and its pull to par, the just-paid dividend trap, graph colouring by backtracking, which tests see a d1/d2 swap, quadrature weights as dual-basis coordinates, a square root by matching parts). `fresh-check --file` on each exam: no hit on a new item. A first draft of the tp-replicate item, a one-step digital at 2%, matched trees `homework-1` items[4] and was replaced by the capped note.

## Minutes

Unchanged for the five 30-item exams. topic-1.8: 28 to 29 items, 60 x 29/28 = 62.1, rounds to 60, so `minutes` stays 60 (no hours change).

## Gates

- `node tools/validate.mjs`: 0 errors; no warning on a new item.
- `VOICE_BASE=app/content/exams python3 docs/reviews/voice-scan.py 35`: 0 explanations over three sentences, 0 sentences over 35 words.
- `grade-all.mjs --file` on each of the six exams: 0 failures.
- `playthrough.mjs --exam <id>` desktop and `--mobile` for all six: all passed. Mobile screenshots read; the C++ test options of e-swapped-d were clipped at 440 px and were rewrapped to 30 characters a line, then replayed green.
