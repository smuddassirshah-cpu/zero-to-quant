# Concept audit (blind): six Fluency sets, number-sense and markov

Auditor: blind Fable reader, 26 Nov 2026, at commit `96f27071`. Scope: `app/content/courses/number-sense/` `fluency-l3-adding-pieces`, `fluency-l5-how-many-halves`, `fluency-l8-below-zero`, `fluency-l9-negative-times-negative`, `fluency-l12-which-first` (Stage 0, reduced ledger depth) and `app/content/courses/markov/fluency-l2-transition-matrix` (Stage 1, full depth). Sixteen generated families.

Blind rule kept: the ledger, the findings and the concepts script were written before any earlier read was opened (`docs/reports/fluency-number-sense.md`, `docs/reports/fluency-markov.md`, `docs/reviews/audit-markov-1-3.md` and `-r2.md`, which name the markov set). Only the lessons `l3-adding-pieces`, `l5-how-many-halves`, `l12-which-first` and markov `l2-transition-matrix` were opened, to read the convention each set inherits.

## Result

- Ledger: `docs/reports/audit-fluency-ns-markov-ledger.md`, 81 rows: 73 correct, 3 imprecise, 4 misleading, 1 wrong, 0 unverified.
- Findings: 7. 1 `wrong`, 2 `imprecise`, 4 `misleading`. 2 `serious`, 5 `minor`.
- No key is wrong on any draw of any family, and no slip value differs from the mistake its line names. No slip band reaches a key. Every markov matrix has rows that sum to 1 and every markov key follows the row-vector convention the lesson states.
- The two serious findings are one fault in two files: the fraction families mark a mixed number wrong, the lessons teach and accept it, and the prompt does not say which form is wanted.

## Method

Every family was judged over its whole range, not a draw. `docs/reports/fluency-ns-markov-concepts.py`:

- Part A reads only the `vars` of each family and enumerates every combination (152 to 2,432 per family, 10,895 kept draws in all). The key, each slip, each `when` and each `where` are derived again in exact fractions from the vars, never from the file's `let`. Per draw it checks the key, each offered slip against the mistake its line names, each slip band against the key and against the other slips, and each rule the feedback states (direction words against signs, the sign rules, lowest terms of the drawn fractions, rows summing to 1, the row of P² and the moved distribution summing to 1).
- Part A2 lists the draws on which a slip is switched off by `when` because the named wrong method gives the key.
- Part A3 counts the keys that are fractions above 1.
- Part B draws 300 items per family with `tools/fluency-sample.mjs --json` and compares the printed key and slips with the Part A derivation from the printed vars: 4,800 draws, 0 mismatches, every printed fraction key in lowest terms.
- The mixed-number claim was run, not read: a scratch widget with key `\frac{17}{12}`, `form: fraction` and `accept: ["1\frac{5}{12}"]` through `grade-all.mjs` returns `accept-refused ... (key "form")`; the same widget without `form` accepts it.

Sources: Norris, *Markov Chains*, section 1.1 (Theorem 1.1.3) for the n-step chance as an entry of Pⁿ and the distribution as a row vector times P; the usual order of operations (brackets, powers, then multiplication and division from left to right, then addition and subtraction from left to right).

## Findings

1. `number-sense/fluency-l3-adding-pieces.json` | `families[add-unlike].prompt` (with `widget.form`) | imprecise, serious | The prompt asks for "a fraction in its lowest terms". On 228 of 456 draws the key is above 1 (as $\tfrac{17}{12}$). `form: "fraction"` grades the mixed number $1\tfrac{5}{12}$ wrong, and Fluency gives no second try. Lesson `l3` teaches that $\tfrac{5}{4}$ is "written $1\tfrac{1}{4}$ as a mixed number", and its quiz accepts $1\tfrac{1}{2}$. About five questions in an attempt have such a key and the pass mark allows two misses, so a learner who writes the taught form fails the set with every sum right. | Evidence: script Part A3; scratch widget through `grade-all.mjs`; `l3-adding-pieces.json` `screens[5].explain.text`, `quiz[2].widget.accept`. Basis: a mixed number in lowest terms is a correct value in a notation the lesson gave; the item does not state the convention it grades. | Fix, `prompt`: `Work out $\\tfrac{{{a}}}{{{b}}} + \\tfrac{{{c}}}{{{d}}}$ as one fraction in its lowest terms, not a mixed number.` (`subtract-unlike` needs no change: its keys are all below 1.) An engine option that accepts a mixed number is raised in the inbox.

2. `number-sense/fluency-l5-how-many-halves.json` | `families[whole-by-fraction].prompt`, `families[fraction-by-fraction].prompt` | imprecise, serious | The same fault. "A whole number or a fraction in its lowest terms" does not rule out $4\tfrac{1}{2}$ for $\tfrac{9}{2}$, which is graded wrong. 58 of 152 and 149 of 259 draws have a key that is a fraction above 1. Lesson `l5` `screens[3]` accepts "$\tfrac{3}{2}$, $1\tfrac{1}{2}$ or 1.5". | Evidence: script Part A3. | Fix, both prompts: replace `as a whole number or a fraction in its lowest terms.` with `as a whole number or one fraction in its lowest terms, not a mixed number.`

3. `number-sense/fluency-l12-which-first.json` | `families[brackets-first].wrong` (`added-first`, `multiplied-then-squared`) | wrong, minor | The two slips are the same number when $a = 8$, $b = 3$ and the bracket is 2 (7 of 1,008 draws, as $8 + 3 \times (5 - 3)^2$): $(8 + 3) \times 4 = 44$ and $8 + (3 \times 2)^2 = 44$. A learner who squared $3 \times 2$ is told "You added $8 + 3 = 11$ first", a mistake they did not make. `grade-all.mjs` reports it only as "1 coinciding Fluency draws noted". | Basis: $(a + b)g^2 = a + b^2g^2$ needs $a(g^2 - 1) = b(b - 1)g^2$; in range only $g = 2$, $b = 3$, $a = 8$ (enumerated). | Fix: add to the family `"where": ["(a + b)*g^2 != a + (b*g)^2"]`. Tried on a scratch copy: draws complete, 179 distinct prompts in 200.

4. `number-sense/fluency-l3-adding-pieces.json` | `families[subtract-unlike].wrong[1]` (`tops-not-renamed`, its `when`) | misleading, minor | On 12 of 228 draws, keeping the old tops gives the key: $\tfrac{2}{3} - \tfrac{1}{2}$ has $\tfrac{2 - 1}{6} = \tfrac{1}{6}$, which is right. The `when` switches the slip off there, so the wrong method scores and the learner's habit is confirmed. | Evidence: script Part A2 (12 draws listed by rule $u - w = a - c$). | Fix: add `"(a - c)/lcm(b, d) != a/b - c/d"` to the family's `where` and drop the `when` of `tops-not-renamed`. Tried on a scratch copy: draws complete, 131 distinct prompts in 200, 604 of 804 tries rejected (75%, under the validator's 80% limit; do not add a further condition to this family).

5. `markov/fluency-l2-transition-matrix.json` | `families[two-state-two-step].wrong[0]` (`squared-entry`, its `when`) | misleading, minor | On 8 of 288 draws, squaring the single entry gives the key. With $a = 0.1$, $b = 0.2$, bull to bear: the entry is 0.9, and $0.1 \times 0.9 + 0.9 \times 0.8 = 0.81 = 0.9^2$. The slip is switched off and the wrong method scores. | Basis: for $i \ne j$, $p_{ij}^2 = (P^2)_{ij}$ exactly when $p_{ii} + p_{jj} = p_{ij}$; enumerated in the script. | Fix: add `"sq != key"` to the family's `where` and drop the `when` of `squared-entry`. (The `when` of `one-step` is always true, since $P^2 = P$ entrywise only when the rows are equal, which `a != b` excludes; it can stay.) Tried on a scratch copy: 144 distinct prompts in 200.

6. `markov/fluency-l2-transition-matrix.json` | `families[three-state-two-step].wrong[1]` (`one-step`, its `when`) | misleading, minor | On 10 of 648 draws the two-step chance equals the one-step chance (first: rows (0.5, 0.4, 0.1), (0.3, 0.4, 0.3), (0.2, 0.4, 0.4), Sunny to Cloudy: 0.4 both ways). Reading the entry off the matrix scores, and the question does not test the skill in its heading. | Evidence: script Part A2. | Fix: add `"where": ["p1j != key"]` to the family and drop the `when` of `one-step`. Tried on a scratch copy: 171 distinct prompts in 200.

7. `number-sense/fluency-l8-below-zero.json` | `families[subtract-signed].wrong[1].line` (`reversed`) | misleading, minor | "You took ${a}$ from ${b}$. The first number is where you start." The value $b - a$ is the key with its sign flipped, so the line is arithmetically true on every draw. On 435 of 765 draws the same number is what dropping the signs gives ($-5 - 3$ typed as 8; $-5 - (-3)$ typed as 2), the likelier slip there. That learner is told they took $-5$ from $3$, which they did not do. | Evidence: script, Info line. | Fix, `line`: `The size is right but the sign is not: that is ${b:()} - {a:()}$. Start at ${a}$ and move ${m}$ to the {dir}.` Basis: $b - a = -(a - b)$ on every draw, and the key is never 0 (`a != s*m`).

## Checked and found sound

- l3: the mediant $\tfrac{a+c}{b+d}$ never equals the sum, the two slips never meet, and two reduced fractions with different bottoms never sum to a whole number, so "a fraction" is always true of the key.
- l5: the three slips and the key are pairwise different on every draw; "dividing by it is multiplying by its upside-down" holds on every draw.
- l8: the direction word matches the sign on all 1,440 kept draws of both families.
- l9: "two negatives give a positive, one negative gives a negative" and "division follows the same sign rules" hold on every draw; the `upside-down` band of 0.005 holds a 2-place decimal of every $1/q$ and never reaches the key.
- l12: `left-to-right`, `lost-sign`, `multiplied-then-squared`, `doubled`, `right-pair-first` and `minus-lost` never equal the key or each other; $a \div b \times c$ is keyed left to right, the standard convention and the lesson's.
- markov: rows sum to 1 and entries lie strictly between 0 and 1 on every draw; keys are entries of P² and of π₀P (row vector on the left, as lesson `l2` states); every key has at most two decimal places, so tolerance 0 and "exactly" are sound.

## Overlap with earlier reads

Opened after the ledger and findings were written: `docs/reports/fluency-number-sense.md` and `docs/reports/fluency-markov.md` (author reports), `docs/reviews/audit-markov-1-3.md` and `docs/reviews/audit-markov-1-3-r2.md` (both had the markov set in scope; ledger rows 36 to 38 of the r2 ledger mark all three families correct, with "each guarded by `when`" as the basis). No review or audit had read the five number-sense sets.

| | count |
|---|---|
| found by this audit only | 7 |
| found by an earlier read only | 0 |
| found by both | 0 |

New `wrong`: 1 (finding 3). Notes on the earlier reads: the author report says keys above one whole "stay improper, as in the lesson"; the lesson's own quiz accepts the mixed number (findings 1 and 2). The author fixed three coinciding slip pairs "on reading" and missed the one in finding 3, which only an enumeration of the range shows. The earlier markov audits read the `when` guards as a safeguard; findings 5 and 6 are the draws on which the guard means a wrong method is marked right.

## Gates

- `docs/reports/fluency-ns-markov-concepts.py`: exit 1, 5,511 checks passed and 7 left failing on purpose (finding 3: one; finding 4: one; findings 5 and 6: one each; findings 1 and 2: three, one per family). Each turns green when its fix is applied. Venv Python; nothing depends on a package version (standard library only, plus node for Part B).
- Validator: 0 errors (4,615 warnings), manifest unchanged.
- `run-number-scripts.mjs --only number-sense`: 7 of 7 passed. `--only markov`: 5 of 5 passed.
- `grade-all.mjs --file` on each of the six files, `--fluency-seeds 40`: 0 failures each; `fluency-l12-which-first` prints "1 coinciding Fluency draws noted" (finding 3).
- No playthrough, as the auditor rules set.

## Fix pass

Opus fixer, 26 Nov 2026, from commit `724091bb`. Every change was checked over the family's whole range by my own enumeration in exact fractions (scratch `fix-fluency/ranges_check.py`), then by the engine's sampler.

1. Fixed. `add-unlike` prompt now ends "as one fraction in its lowest terms, not a mixed number." Basis: `shapeFraction` in `js/engine/grade.js` accepts only a whole number or a single `\frac{p}{q}` (or `p/q`) in lowest terms, so `1\frac{5}{12}` fails the shape; 228 of 456 draws have a key above 1, none whole; lesson `l3` quiz `accept` lists $1\tfrac{1}{2}$. `subtract-unlike` keys are all below 1 (216 kept draws), so its prompt is unchanged.
2. Fixed. Both `l5` prompts now read "as a whole number or one fraction in its lowest terms, not a mixed number." Basis: same grader; 58 of 152 and 149 of 259 draws have a non-whole key above 1 (enumerated); lesson `l5` accepts $1\tfrac{1}{2}$.
3. Fixed. `brackets-first` gains `"where": ["(a + b)*g^2 != a + (b*g)^2"]`. Basis: equality needs $a(g^2 - 1) = b(b - 1)g^2$; enumerating $g = 2, 3, 4$ and $b = 2$ to 5 leaves only $a = 8$, $b = 3$, $g = 2$ (7 of 1,008 draws). Neither slip equals the key on any draw ($g \ge 2$, $b \ge 2$), slips carry no band and the key tolerance is 0. 1,001 draws kept, 179 distinct prompts in 200; 5,000 sampler draws hold no $(8, 3, 2)$.
4. Fixed. `subtract-unlike` gains the `where` `(a - c)/lcm(b, d) != a/b - c/d` and `tops-not-renamed` loses its `when`. Basis: enumerated, 12 of 228 draws have $\tfrac{a - c}{L}$ equal to the key (first $\tfrac{2}{3} - \tfrac{1}{2}$). I also checked the other `when` (`tops-and-bottoms`): its key-guard part never fires (0 draws), and $a > c$, $b > d$ is a shape condition, so it stays. 216 draws kept; validator sample 604 of 804 tries rejected (75%, under 80%), 131 distinct prompts in 200.
5. Fixed. `two-state-two-step` `where` becomes `["a != b", "sq != key"]` and `squared-entry` loses its `when`. Basis: enumerated, 8 of 288 draws (first $a = 0.1$, $b = 0.2$, bull to bear: $0.9^2 = 0.81 = (P^2)_{01}$). `one-step`'s `when` is always true ($P^2 = P$ entrywise only when $a = b$, enumerated) and stays. 280 draws kept, 144 distinct prompts in 200.
6. Fixed. `three-state-two-step` gains `"where": ["p1j != key"]` and `one-step` loses its `when`. Basis: enumerated, 10 of 648 draws; `squared-entry` never equals the key (0 draws), so its `when` stays. 638 draws kept, 171 distinct prompts in 200.
7. Fixed. `reversed` line now: "The size is right but the sign is not: that is ${b:()} - {a:()}$. Start at ${a}$ and move ${m}$ to the {dir}." Basis: the slip value is $b - a = -(a - b)$ on all 765 draws and the key is never 0 (`a != s*m`), so the line is true whichever slip produced the number; 435 of 765 draws match a dropped-signs value (enumerated), so the old line named the wrong mistake there.

No key, slip value or test changed; four `when`s removed, four `where` conditions added, three prompts and one line reworded. Distinct prompts stay far above the set's n of 20.

Scripts re-pointed: `docs/reports/fluency-ns-markov-concepts.py` (the four models now reject the draws the new `where` drops; new Part A4 checks each file carries the `where` and no `when`; docstring says so) and `docs/reports/fluency-number-sense-numbers.py` (prompt text of three families; `tops-not-renamed` always offered, with a check that it never gives the key).

Gates: concepts script exit 0 (5,521 checks); validator 0 errors, output identical to the pre-fix run; voice scan 35 on the five files 0 and 0; `run-number-scripts --only number-sense` 7 of 7, `--only markov` 5 of 5; `grade-all --file --fluency-seeds 4` (and 40) 0 failures on all five, no coinciding-draw note on l12; `test-fluency` l3 and l5 300 of 300; playthrough `--fluency` of the five sets desktop and `--mobile` all passed.

## Fix-pass read

Fresh reader, blind to the audit above until the rows were written. Diff read: `git show 88c4cbe3 -- app/content/courses` at HEAD 812bfa4b. Basis for every row: a full-range enumeration of the family's `vars` in exact fractions, written from the vars alone (not from the committed `let`s or scripts), and the real `gen.js` and `grade.js` with the local Compute Engine on every distinct draw of 4,000 seeds. Scratch scripts: `fullrange.py`, `more.py`, `grade.mjs` in `scratchpad/fpr-fluency/` (not committed).

| # | file | JSON path | claim | verdict | basis |
|---|------|-----------|-------|---------|-------|
| 1 | markov/fluency-l2-transition-matrix | families[two-state-two-step].where `sq != key` | Removes exactly the draws where the squared entry is the two-step chance | correct | 324 draws: 36 have a = b, 8 have sq = key, 280 kept, all distinct. The 8 are (a, b, i, j) = (0.1, 0.2, 0, 1), (0.2, 0.4, 0, 1), (0.3, 0.6, 0, 1), (0.4, 0.8, 0, 1), (0.2, 0.6, 1, 0), (0.4, 0.7, 1, 0), (0.6, 0.8, 1, 0), (0.8, 0.9, 1, 0). On the 280: sq is never the key and never the one-step value; the one-step value is never the key (P² − P = (a − b)(a − b − 1)Q with no zero entry, so its `when` never bites). Rejection 13.6% of the range, 11.9% at the validator's 200 seeds (limit 80%). Both slips grade to their own id on all 280. |
| 2 | same | families[two-state-two-step].wrong[squared-entry] (`when` removed) | The slip is offered on every draw and is wrong on every draw | correct | Row 1: sq ≠ key on all 280 kept draws. |
| 3 | same | families[three-state-two-step].where `p1j != key` | Removes exactly the draws where tomorrow's chance is the two-day chance | correct | 648 draws: 10 have p1j = key (all with first row 0.5, 0.4, 0.1 or similar and j = 2), 638 kept, all distinct. On the 638: p1j ≠ key, sq ≠ key, sq ≠ p1j. Rejection 1.5% (2.9% at the validator's seeds). Both slips grade to their own id on the 636 distinct draws sampled. |
| 4 | same | families[three-state-two-step].wrong[one-step] (`when` removed) | Offered and wrong on every draw | correct | Row 3. |
| 5 | number-sense/fluency-l12-which-first | families[brackets-first].where `(a + b)*g^2 != a + (b*g)^2` | Removes exactly the draws where the two slips are one number | correct | 1,008 draws: the slips coincide only at (a, b, g) = (8, 3, 2), where both are 44, for the 7 values of d. 1,001 kept, all distinct. Neither slip is the key anywhere (a(g² − 1) > 0 and bg²(b − 1) > 0). Rejection 0.7%. Both slips grade to their own id on all 982 distinct draws sampled. |
| 6 | number-sense/fluency-l3-adding-pieces | families[add-unlike].prompt | "as one fraction in its lowest terms, not a mixed number" matches what is graded | correct | 456 kept draws: 228 keys are top-heavy, none is a whole number (a sum of two lowest-terms fractions with different bottoms is never 1). Grader: the top-heavy key passes as `\frac{p}{q}` and `p/q` on all 456; `1\frac{1}{8}`, `1 \frac{1}{8}` and `1+\frac{1}{8}` return `form` on all 228; unreduced and decimal forms return `form`. Slips: never the key, never each other, each to its own id. |
| 7 | same | families[subtract-unlike].where `(a - c)/lcm(b, d) != a/b - c/d` | Removes the draws on which "common bottom, old tops" gives the key | imprecise (minor) | It removes exactly the 12 draws it names (2/3 − 1/2, 3/4 − 2/3, 2/5 − 1/3, 4/5 − 1/2, 4/5 − 2/3, 4/5 − 3/4, 5/6 − 4/5, 7/8 − 2/3, 2/9 − 1/6, 8/9 − 1/2, 8/9 − 3/4, 9/10 − 2/3) and no others; 216 kept, all distinct; rejection 74.3% of the range, 75.1% at the validator's seeds. But the same slip over the other natural common bottom, b × d, still gives the key on 21 of the 216 kept draws (9.7%): for example 5/6 − 3/4 gives (5 − 3)/24 = 1/12, which is the key; 3/4 − 1/2 gives 2/8 = 1/4; 11/12 − 2/3 gives 9/36 = 1/4. A learner who multiplies the bottoms and keeps the old tops is marked right there. Fix below. |
| 8 | same | families[subtract-unlike].wrong[tops-not-renamed] (`when` removed) | Offered and wrong on every draw | correct | (a − c)/lcm ≠ key on all 216; it grades to its own id on all 216, including the 72 draws where its top is zero or negative; it never equals `tops-and-bottoms` where that is offered (102 draws). |
| 9 | same | families[subtract-unlike].prompt (unchanged, read in context) | Needs no mixed-number clause | correct | Every key is strictly between 0 and 1 on all 216 draws. |
| 10 | number-sense/fluency-l5-how-many-halves | families[whole-by-fraction].prompt | "a whole number or one fraction in its lowest terms, not a mixed number" matches what is graded | correct | 152 draws, all distinct: 94 whole keys, 58 top-heavy, none proper. Key passes on all 152; the three mixed forms return `form` on all 58. Slips never the key or each other; `bottom-only` offered on the 88 draws with a > 1. |
| 11 | same | families[fraction-by-fraction].prompt | Same sentence | correct | 259 kept draws: 31 whole, 149 top-heavy, 79 proper. Key passes on all 259; mixed forms return `form` on all 149. Slips never the key or each other. Rejection 4.1%. |
| 12 | number-sense/fluency-l8-below-zero | families[subtract-signed].wrong[reversed].line | "The size is right but the sign is not: that is b − a. Start at a and move m to the {dir}." | correct | 765 kept draws: flip = b − a = −key with key ≠ 0 on every one (a ≠ b by `where`), so the size matches and the sign does not; a moved m to {dir} is the key on every one; flip is never `added` (that needs a = 0). The line stays true when the learner reached the value another way (|a| + m is the same number on 225 draws), which the old line was not. Drawn text reads "that is $6 - 1$" and brackets a negative. |
| 13 | app/js/engine/grade.js | `shapeFraction`, `FORM_LINE.fraction` | `form: fraction` refuses a mixed number and accepts the top-heavy fraction | correct | Rows 6, 10, 11 through `exprGrade`. The line shown is "That is equal, but write it as a whole number or one fraction in lowest terms, with no decimal point.", which agrees with the new prompts. Two edges for the engine inbox are below. |

Counts: 13 rows; 12 correct, 1 imprecise (minor), 0 wrong, 0 misleading, 0 unverified.

Rejection and supply: every changed family is under the 80% limit at the validator's 200 seeds (two-state 11.9%, three-state 2.9%, brackets-first 0%, subtract-unlike 75.1%) and has at least 216 distinct draws for at most 10 turns in an attempt of 20.

### Fix for row 7

`number-sense/fluency-l3-adding-pieces.json`, `families[subtract-unlike].where`, paste-ready:

```json
"where": ["b != d", "lcm(b, d) <= 36", "a*d > b*c", "(a - c)/lcm(b, d) != a/b - c/d", "(a - c)/(b*d) != a/b - c/d"],
```

Basis: enumeration leaves 195 distinct draws, none with (a − c)/lcm or (a − c)/(b × d) equal to the key. Tried on a scratch copy with the real generator: 77.5% rejected at the validator's 200 seeds (124 distinct prompts), 77.2% over 4,000 seeds, no failed draw. That is under the limit but only by 2.5 points. The audit (finding 4) advised no further condition on this family at 75%; this one was measured, and anything beyond it should shorten the two `pick` lists instead. The add family needs no such line: (a + c)/(b × d) is never the key there.

### Seen while enumerating, outside the diff (for the orchestrator to rule on)

1. `fluency-l12-which-first`, `brackets-first`: on the 329 kept draws with a bracket worth 2, doubling in place of squaring gives the key (2² = 2 × 2). `powers-next` in the same set names that slip (`doubled`, `when: c != 2`). If the rule of this fix pass (no draw on which a named wrong method gives the key) is meant to reach it, `"g": { "int": [3, 5] }` removes it and leaves 1,344 draws less any coincident slips; I have not enumerated that range.
2. `markov/fluency-l2-transition-matrix`: on a symmetric matrix a row is a column, so reading P the wrong way round, or multiplying row by row, gives the key. Two-state: 32 of 280 kept draws (a + b = 1). Three-state: row times row gives the key on 84 of 638, and twice the one-step chance on 12. None is a named slip.
3. Engine, plain-text fallback only (no maths field): a mixed number typed as `1 3/10` is read as `13/10` once the space is dropped, so it passes on the 16 add-unlike and 4 fraction-by-fraction draws with bottom 10, and `1 1/36` (key 37/36) is read as 11/36 and gets the `tops-not-renamed` line on 2 add-unlike draws. Other text mixed numbers are refused with no line. `1\tfrac{1}{8}` is refused with no line; `\frac` forms get the `form` line.
4. Two `when`s left in place are never false on the kept draws (two-state `one-step`, three-state `squared-entry`). They are harmless.
