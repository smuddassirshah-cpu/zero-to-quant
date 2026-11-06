# Topic 0.6 exam: reasoning and proof

File: `app/content/exams/topic-0.6.json` (60 minutes, pass 0.7, 24 items, all six skills of `proof`). Scripts: `docs/briefs/exam-0.6-scripts/` (`build.py` route A, `check_numbers.py` route B, `fresh.py`).

## Result

- Ramp 5, 12, 5, 2 at difficulties 2 to 5; pace 3,150 s (53 min).
- By level: L1 5 items (pv-logic), L2 7 (pv-sets, and pv-direct in the element chase), L3 12 (pv-direct, pv-indirect, pv-induction, pv-writing). Every level has an item on a skill first met there.
- Kinds: 9 numeric, 9 choice, 3 order, 1 table, 1 parts (numeric then choice), 1 longform (self-marked induction, rubric 10). Every skill is also on an auto-graded item; pv-induction and pv-writing on three or more each.
- Order proofs: an element chase (L2), a forwards proof of $x + 1/x \ge 2$, and $4m + 3$ is never a sum of two squares. Each has two distractor lines with a `why`.

## Gates

- Validator: 0 errors, no topic-0.6 warnings.
- Voice scan on a copy: 0 and 0. No em-dashes or exclamation marks.
- `check_numbers.py`: 141 of 141, exit 0. Truth tables and function counts by enumeration, sets as Python sets, Fractions, brute-force searches for the counterexample and the base case, and each induction step checked as an identity at many $k$.
- Playthrough with `--local-cdn`: green with and without `--mobile`; screenshots checked (table, order and parts at 440 px).

## Freshness

Four clashes were changed. `n^2 - n + 11` and "no smallest positive rational" are both in proof homework-3's longform, so they became $n^2 + n + 17$ and rational plus irrational. $x^2 = 5x$ divided by $x$ is the quadratics l5 trap, so it became a write-up that proves the converse. $A \cap (B \cup C)$ is the l7 tap set, so the chase became $(A \cup B) \cap C \subseteq (A \cap C) \cup B$. Other hits are common words or numbers in unrelated settings.
