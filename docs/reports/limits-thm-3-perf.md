# limits-thm level 3: performance task (PLAN 2a Phase 3 retrofit)

- File: `app/content/courses/limits-thm/homework-3.json`, item `h-prove-desk-guarantee`, index 9 (item 10 of 10; the homework had 9, nothing converted).
- Kind `derivation` (longform, empty box), difficulty 5, skill `dl-lln`.
- Matched objective: l10 "Derive Markov from an indicator bound and Chebyshev from Markov". It is the only objective of the level that starts with derive (l9 see, show; l11 watch; l12 use; l13 approximate).
- Task: independent bets that need not share a distribution, each with variance at most $v$. (a) Markov from the indicator; (b) Chebyshev in $\epsilon$ form from (a); (c) the law for the average of non-identical bets, $\le \tfrac{v}{n\epsilon^2}$, saying where independence and the cap are used (a counterexample without a cap: $\sigma_i^2 = i$ gives $\tfrac{n+1}{2n} \to \tfrac12$); (d) a book of $n$ bets of each of two kinds (±£1 at 0.55; +£3 or −£1 at 0.3). Chebyshev on the one-sided event needs $n = 967$; a normal model (CLT within each kind, a sum of independent normals) needs about 131; an exact computer sum gives 136.
- Rubric 2, 2, 2, 3, 1. Rows 1 to 4 are `required` (9 points), one for each of (a) to (d). `rubric-passes.mjs`: the only minimal pass is rows 1 to 4. Only row 5 (the normal-model estimate) can be left out.
- Overlapping screens: l10 screens 2 and 5 (Markov and Chebyshev in $k\sigma$ form, ordered), screen 9 (smallest $n$ from Chebyshev on an average); `h-wlln-proof` (the weak law for identical draws, ordered); l9 screen 5 (variance of an average); l11 screens 7 and 9, `h-insurer`, `r-trades-loss` (normal sums of identical bets). New: both proofs from a blank box, the law for bets that do not share a distribution, with the cap's role and a counterexample, a one-sided event held inside a two-sided one, two kinds of bet, and a normal model justified kind by kind.
- Freshness grep (course folder, every hit read): `967`, `131`, `136`, `4.35`, `3.36`, `0.99`, `0.55`, `£3`, `need not`, `same distribution`, `not identically`. Only stock values (Bin(20, 0.55), data tables) are shared. `fresh-check.mjs --file content/courses/limits-thm/homework-3.json`: 1 hit, `exact_tail` in the existing `h-tail-code` against l19, and none on the new item.

## Gates

1. `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors. Expected warning "limits-thm/L3: has a performance task, remove from perf-pending". Manifest restored before commit.
2. `VOICE_BASE=app/content/courses/limits-thm python3 docs/reviews/voice-scan.py 35`: 0 and 0.
3. `<venv>/bin/python -I docs/reports/limits-thm-3-perf-numbers.py`: exit 0, 67 checks. Markov and Chebyshev exactly on 300 random laws; a mixed book simulated against $\tfrac{v}{n}$; exact rationals for (d). $P(S \le 0)$ by integer binomial sums and by scipy, which agree. Seeded simulations ($2 \times 10^6$ books at $n = 131$ and $136$). The normal $n$ by scipy and by the 1.645 cut-off. Passing tick sets listed.
4. `node tools/playthrough.mjs --set limits-thm/homework-3 --local-cdn <pkgs>`, with and without `--mobile`: All passed, 2 longform marked by the button. The 356 px KaTeX column check and its shot showed every display inside the column. The tool's one "scrolls" line is its known misreading of a `\sqrt` display.

One backlog bullet, under "Raised later (limits-thm level 3 perf):". No course.json change.
