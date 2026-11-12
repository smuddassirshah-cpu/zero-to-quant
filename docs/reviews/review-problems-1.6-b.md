# Problem sets 1.6 (b), testing levels 1 to 3: second-reader findings

Scope: `app/content/courses/testing/problems-1.json`, `problems-2.json` and `problems-3.json`: 12 problems, 54 parts (43 typed, 11 choice). `problems-4.json` was read before (`review-holes-1.6-2.1.md`) and is not in scope. Patterns: `review-problems-1.5-a.md`, `review-holes-1.6-2.1.md`, `review-delta-holes.md`.

Method. The author's script was run first. The twelve lessons l1 to l12 were then skimmed screen by screen (`taught.py`) for what each level teaches, its notation and its decision rule ($p \le \alpha$ in l3, "centred" in l6, $n = 6.18(\sigma/\delta)^2$ in l6, $\mathrm{SR}\sqrt T$ in l11, Šidák in l10, the bars of 2 and 3 in l12). Every part was solved from its text before its answer was read, by hand and again in `review-problems-1.6-b-scripts/mine.py`, which imports nothing from the author's script and types its inputs from the prose: SciPy's normal, $t$ and binomial tails, `ttest_1samp`, `ttest_ind_from_stats`, statsmodels `multipletests`, exact fractions for the 4096 sequences, a noncentral $t$ for the true power of the shoe trial. Every `wrong` value was re-derived from the slip its line names, and every number printed in a `feedback` or `explain` string was recomputed. Each of the 43 typed parts then went through the engine's own grader in node (`grade-probe.mjs`: `numGrade` of `app/js/engine/grade.js`): the stored answer, every `wrong` entry on its own key, and 4 to 12 strings of my own a part (a fraction for a decimal, more places, a % sign, a unit, a letter and `=`, a true minus sign, the value the part's own working prints, the value one place short, each slip as a learner would round it).

Tags: `wrong` = a learner is marked wrongly or told something false; `unclear` = the question can be read two ways or does not say the form wanted; `minor` = weak part, loose `wrong` entry, missing hypothesis, label or freshness.

## Tool results

| check | result |
|---|---|
| author's script `problems-testing-numbers.py` (scratchpad venv) | 1,019 checks, 0 failures, exit 0 |
| `mine.py` (reader's own keys, slips, stated numbers, set shape) | 635 checks, 0 failures; 7 notes read (findings 5, 7) |
| `grade-probe.mjs` (engine grader, 43 typed parts) | 674 checks, 0 failures, 10 rows held to be faults (findings 3, 4, 5, 6) |
| `proposed.py` (numbers of the fixes below) | 20 checks pass |
| `fresh.py` (story nouns, data and parameters against the course and exams `topic-1.6`, `stage-1`) | read by hand; finding 9 |
| validator | 0 errors; no warning on the three files; `manifest.json` unchanged |
| playthrough `--problems` 1, 2, 3 with `--local-cdn` | all passed, desktop and `--mobile` |
| voice scan 35, `testing` | 0 explanations over three sentences; 1 sentence over 35 words, in `homework-3.json` (not in scope) |
| `fresh-check.mjs --file` 1, 2, 3 | 0 hits; 6, 6 and 9 advisories, all shared constants (0.05, 1.96, 1.645, 6.18, 0.0455) |

Result. All 54 keys agree with mine, and so does every one of the 111 `wrong` values and every number in a feedback or explanation string. No `wrong` finding: no part marks a right answer wrong in the form it asks for, no band takes in a wrong method, and no statement of theory is false. One question's wording favours an answer the part refuses (finding 1). The rest are loose slip bands, two parts that hand over their answer, missing hypotheses and tasks reworked from lessons.

## Findings

1. `unclear` | `testing/problems-3.json` | `p-checkout-designs` | part 2.
   "How small must $p$ be for that chance to be at most 0.05? Give 6 decimal places." The threshold is $1 - 0.95^{1/25} = 0.00204963$. The key 0.002050 is that value rounded up, and a best p-value of 0.002050 gives a family chance of 0.050009, over 0.05. A learner who reads "at most" with care rounds down to 0.002049, and the grader refuses it (band $5 \times 10^{-7}$).
   Fix: ask for the equality. Question: "Part 1's chance is $1 - (1 - p)^{25}$ for a best p-value of $p$. For what $p$ is that chance exactly 0.05? Give 6 decimal places." Key, band, feedback and `wrong` lines stay.

2. `minor` | `testing/problems-2.json` | `p-fertiliser-trials` | parts 2 and 4.
   Each question tells the learner one value of $\Phi$, and that value is the answer: "You are told $\Phi(0.605) = 0.7274$" (key 0.7274) and "You are told $\Phi(1.537) = 0.9379$. What is its power?" (key 0.9379). Part 4 also gives the centre $2.25\sqrt 2$. The step the parts are about, the cut-off's distance below the centre, is never asked for (the class of `review-problems-1.5-a.md` finding 11).
   Fix: give a second value so the learner must choose. Part 2: "You are told $\Phi(0.605) = 0.7274$ and $\Phi(2.25) = 0.9878$." with a new `wrong` entry `{ "id": "centre-only", "value": 0.9878, "tol": { "abs": 0.00005 } }`: "That is $\Phi$ at the centre itself. Power is the area past the cut-off, so subtract 1.645 first: $\Phi(2.25 - 1.645)$." Part 4: "You are told $\Phi(1.537) = 0.9379$ and $\Phi(3.182) = 0.9993$." with `centre-only` 0.9993: "That is $\Phi$ at the centre, 3.182. Subtract the cut-off first: $\Phi(3.182 - 1.645) = \Phi(1.537)$."

3. `minor` | `testing/problems-1.json` | `p-wine-taster` | part 2.
   The `carried` value is 0.0190 ($\tfrac{78}{4096} = 0.01904$) with band 0.00005. The right answer cut to 3 places, 0.019, is exactly that value, so a learner whose only fault is one place too few is told "You added 66 to 12, leaving out 12 of 12."
   Fix: `carried` line: "That is $\tfrac{78}{4096}$, from adding 66 to 12 and leaving out 12 of 12, or the right answer cut to 3 places. With all 13 sequences above 10 there are 79, and $\tfrac{79}{4096} \approx 0.0193$ to 4 places."

4. `minor` | `testing/problems-2.json` | `p-running-shoes` | parts 2 and 3.
   The keys are whole (3 and $-4$) and the questions ask for no rounding ("Give a decimal." in part 3), but five slip values carry three places and a band of 0.001. The slip typed to 2 places misses its own line and gets the generic one: 2.83 for `divide-by-n` (2.828), 3.05 for `carried` (3.046), $-1.33$ for `over-sd` ($-1.333$), $-4.24$ for `carried` ($-4.243$). `p-phone-battery` parts 1 and 2 give the same kind of entry a band of 0.005.
   Fix: `tol` `{ "abs": 0.005 }` on `divide-by-n` and `carried` of part 2 and on `over-sd`, `root-eight` and `carried` of part 3. No band then touches another or the key (`proposed.py`).

5. `minor` | three parts | doubled-tail slips stored from the rounded $\Phi$ only.
   `problems-1` `p-pizza-delivery` part 2 `two-sided` (0.0802), `problems-2` `p-blood-screen` part 1 `two-tail` (0.0718), `problems-3` `p-fund-managers` part 2 `two-sided` (0.007), each with band 0.00005. A learner who doubles the tail from a calculator's $\Phi$ gets 0.0801, 0.0719 and 0.0069, which miss the line. The author's report says the bands take the unrounded route "where they differ"; on these three slips they do not.
   Fix: `tol` `{ "abs": 0.0001 }` on the three entries. Each stays clear of its key (0.0401, 0.0359, 0.0035).

6. `minor` | `testing/problems-1.json` | `p-phone-battery` | parts 1, 2 and 5.
   Part 1 asks for the mean "in hours" and has no `unit`, so "18 h" and "18h" will not submit (the field reads a one-letter unit only when it is the part's own). "18 hours" is read. `p-cereal-boxes` part 2 (`unit: "g"`) and `p-running-shoes` parts 1 and 2 (`unit: "s"`) set it.
   Fix: `"unit": "h"` on parts 1, 2 and 5.

7. `minor` | hypotheses left out, four places.
   - `problems-1` `p-pizza-delivery` (16 times, $t_{15}$) and `problems-2` `p-running-shoes` (9 differences, $t_8$) use a $t$ cut-off without saying the data are normal. `p-phone-battery` says it ("Treat the 8 lives as independent draws from a normal distribution"). Fix: pizza prose, add "Treat her 16 times as independent draws from a normal distribution."; shoes prose, add "Treat the nine differences as independent draws from a normal distribution."
   - `p-running-shoes` part 5: $n = 6.18(\sigma/\delta)^2$ is l6's formula for a $z$ test with $\sigma$ known. A paired $t$ test on 25 runners has power 0.783, and first passes 0.8 at 27 (noncentral $t$, `mine.py`). The explanation says the gain "needs only 25 runners". Fix: `explain`: "The paired design uses the sd of a difference, 3 seconds, not the far larger spread between runners. So the normal formula asks for only 25 runners. A $t$ test, with the sd estimated, needs a couple more."
   - `problems-3` `p-biomarker-field` part 5, option `fwer`: "the chance of at least one false find is about 0.64" is $1 - 0.9973^{380} = 0.642$, which needs independent tests. The prose of this item does not say so (the gene and checkout items do). Fix: `why` and `byKey.fwer`: "With 380 independent nulls at 0.0027 each, the chance of at least one false find is about 0.64. A fixed bar does not hold that chance down when hundreds of nulls are tested."
   - `problems-3` `p-gene-screen` part 5: the correct option and the explanation say Bonferroni keeps the chance of any false link "near 5%" and "at about 5%". The promise is "at most 5%" (0.0488 here, and lower still when some genes are linked). Fix: option text "Bonferroni's 2 keep the chance of any false link at most 5%; BH's 5 keep the expected share of false links at most 5%"; `explain` first sentence "Bonferroni holds the chance of even one false link to at most 5%, which costs power."

8. `minor` | two last-but-one results not restated.
   `problems-1` `p-wine-taster` part 4 says "Using parts 2 and 3" and `problems-3` `p-fund-managers` part 3 says "With H's p-value from part 2"; neither gives the values. The brief asks each later part to restate what it needs. In the fund item a learner who took the lower tail in part 2 (0.9965) gets 2 managers and loses part 3 as well.
   Fix: wine part 4: "Part 2 gave $P(W \ge 10) = 0.0193$ and part 3 gave $P(W \ge 9) = 0.0730$. What is the smallest number right that rejects $H_0$ at 5%?" Fund part 3: "... With H's p-value, 0.0035 from part 2, BH at $q = 0.10$ compares ...".

9. `minor` | freshness: three items rework a lesson or exam task with new numbers.
   No story is reused: all twelve settings are new to the course, its reviews, homework and the two exams. The tasks and constants below are not, and `fresh-check` lists them only as shared constants.
   - `problems-3` `p-biomarker-field` parts 1 and 3 are l12 screens 3 and 4 ("How many of 300 noise factors would show $|t| > 2$?", then "$|t| > 3$") with 380 for 300 and the same two tail values, 0.0455 and 0.0027. Parts 2 and 4 are l7's share of significant results that are real. The item joins two lessons; it does not add a step.
   - `problems-3` `p-gene-screen` parts 1 and 2 use 40 tests at 5%: exam `stage-1` `b-forty-tests` has the same family ($0.95^{40} = 0.1285$, and 0.8715 is its `at-least-one` slip) and l10 the same $0.05/40 = 0.00125$.
   - `problems-3` `p-checkout-designs` part 1 is l9 screen 6 (the smallest of 20 noise p-values at most 0.02) with 25 and 0.004; part 2 is `homework-3`'s Šidák threshold to 6 places with 25 for 100; part 4 is part 1 again with 0.03.
   Fix: accept the gene and checkout items (the BH step and the hold-out step are new work). In the biomarker item change the bars so the tail values are not l12's: $|z| > 2.5$ and $|z| > 3.5$ with $P(|Z| > 2.5) = 0.0124$ and $P(|Z| > 3.5) = 0.0005$, and rework the four counts and shares; or accept it and relabel it (finding 10).

10. `minor` | `testing/problems-3.json` | difficulty labels.
    `p-biomarker-field` is the set's only 5. Its parts are two products, two ratios and a choice, all on given rates. `p-gene-screen` (4) has the set's hardest step, BH past a failing rank.
    Fix: label `p-gene-screen` 5 and `p-biomarker-field` 4 (and the two rows of `docs/reports/problems-testing.md`).

11. `minor` | last parts.
    `problems-2` `p-running-shoes` part 5 (the size of a larger trial) is bolted on after the result, part 4; it is the item's only use of l6. `problems-3` `p-checkout-designs` part 4 repeats part 1's sum after the decision in part 3. The brief asks the last part for the result the problem is about.
    Fix: accept both, as `review-problems-1.5-a.md` finding 17 did for a like case; or move the shoe trial's part 5 before part 4 ("before the trial, how many runners would the firm have needed?") so the conclusion comes last.

## Per set

- Coverage: every lesson of each level is drawn on and each problem draws on at least two (level 1: cereal l1 to l3, phone l1, l3, l4, wine l1, l3, pizza l2 to l4; level 2: fertiliser l5, l6, tyres l7, l8, shoes l6, l8, blood screen l5, l7; level 3: genes l9, l10, funds l10, l11, checkout l9, l10, l12, biomarkers l9, l12). l11 enters only through $\mathrm{SR}\sqrt T$ in one part.
- Only taught ideas: one-sided $t$ cut-offs are not in l4 (it uses two-sided 5% only), and every part that needs one is told it. Šidák is in l10 screen 1. The either rule's $1 - 0.95^2$ is given, not asked.
- Chains: all twelve are real chains and every part's result is used later; findings 8 and 11 are the loose links. No opening prose gives away an answer; finding 2 is the two parts that state their own.
- Typed parts: 14 of 18, 15 of 19, 14 of 17. Each `choice` part is a judgement.
- Grader: every answer grades correct as stored, as a fraction, with more places, with a % sign where it is a chance, with a letter and `=` in front, and with the value its own feedback prints. Every part refuses the value one place short of what it asks and each slip. Every one of the 111 `wrong` values lands on its own key and has a `byKey` line; no two bands touch.
- Voice: British English, no exclamation marks, no em-dashes, no explanation over three sentences. No money appears.

## Counts

| tag | count |
|---|---|
| wrong | 0 |
| unclear | 1 |
| minor | 10 |

Clean problems (no finding): `p-cereal-boxes`, `p-tyre-brands`. With one small edit each (a band, a unit, a restated value or a sentence of hypothesis): `p-phone-battery`, `p-wine-taster`, `p-pizza-delivery`, `p-blood-screen`, `p-fund-managers`, `p-gene-screen`.

## Engine

- A `wrong` value stored at the asked rounding can be the key cut one place shorter (0.0190 against 0.0193, finding 3); the validator's `[wrong-band]` and `[tight-band]` rules do not see it.
- The classes of findings 4 to 6 (a slip band narrower than a natural rounding where the question asks no places; a slip stored only from the rounded table value; a named one-letter unit with no `unit`) have each been raised before; see the bullets under `Raised later (review problems testing, vectors):` in `docs/BACKLOG-INBOX.md`.
