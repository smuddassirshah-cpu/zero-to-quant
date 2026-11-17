# Delta read AG, stat-models problems-3: `p-hedge-ranks` re-authored on n = 14

Counts: `wrong` 0, `misleading` 0, `reuse` 0, `re-author` 0, `continuity` 0, `voice` 0, `other` 1. No key and no `wrong` value is mistaken. Verdict on reuse: `clean`. The open bullet of KNOWN_ISSUES "session AF close" (twelve values and a rank sum of 8.5 beside l10 screen 5) is closed by this re-author.

Scope, at commit 7b293c7a ("problems stat-models level 3: p-hedge-ranks re-authored on new data"): `p-hedge-ranks`, all four parts. `p-spread-day-tail` and `p-five-weeks-flip` were read only as reuse sources.

Reviews read: `review-delta-af-stat-models.md` (findings 5 to 7 and the fix pass), `docs/reports/problems-stat-models.md` (session AG section). Exams: the brief's `grep -l stat-models app/content/exams/*.json` matches no file; the course's items carry `sm-` skills and sit in `exams/topic-2.6.json` only, which was read in full for rank, tie and sign items. No stage or mock exam has a signed-rank item (`grep -lE "signed.rank|Wilcoxon|hedging error"` over `app/content`).

Method. Each part was solved from its text before its key was read. No browser, no content or engine edit. Script: `docs/reports/delta-review-delta-ag-hedge-ranks-numbers.py`, 520 checks, exit 0, 1 FINDING line (finding 1); 0 with the fix on a scratch copy.

## Findings

`N. file | JSON path | class | problem | evidence | exact fix`

1. `problems-3.json` | `p-hedge-ranks` `parts[2].explain.text` | other | "half the 105 ranks" reads as a count of ranks. There are 14 ranks; 105 is their total, $14 \times 15/2$. The form came over from the 12-month version ("half the 78 ranks"). Minor: no number is wrong and no learner is refused. | Script, FINDING line 1. | `explain.text`: "With no difference $W^+$ would sit near $14 \times 15/4 = 52.5$, half the rank total of 105. The data give 12.5, which is 40 below. In standard deviations that is $z \approx -2.511$." Tested in place and restored: this script 0 FINDING lines, the author's script 1182 passed, voice 35 0 and 0, `fresh-check --file` 0 hits, `grade-all --file` 0 failures.

## Reuse

| problem | closest lesson screens | closest review, homework, set and exam items | verdict |
|---|---|---|---|
| `p-hedge-ranks` | l10 S5 (signed ranks, $W^-$ of twelve days), l10 S7 prose and quiz 0 (the tie rule), l11 S8 (sign-flip), l9 S5 (sign test) | `r3-paired`, `h-mw-z`, `h-u-moments`, `p-two-looks`, `p-five-weeks-flip`; exam `e-sign-test-ties`, `e-walsh-median`, `e-kruskal-h` | clean |

Both texts, for the three nearest.

- l10 S5: "Rank the absolute returns, then add the negative days' ranks: $W^-$. A has three losing days: $-0.08$, $-0.12$ and $-0.03$." Key 8, slips 70 ($W^+$) and 3 (the count), twelve days, no tie. Set part 1: 14 months, two positive months, a tie, key 12.5, slips 12, 13 and 92.5. The same standard task. It no longer shares the count of values, the statistic's value or its neighbour (8 against 8.5), and it asks for $W^+$ where the lesson asks for $W^-$. The generic line was replaced in fix pass AF and is its own.
- l10 quiz 0: "Pooled returns sorted: $-0.2, 0.1, 0.3, 0.3, 0.5$. What rank does each 0.3 get?", 3.5, slips "You gave both the lower rank." and "You gave both the upper rank." l10 S7 prose: "Two days tied for ranks 5 and 6 each get 5.5." Set: the tie fills places 4 and 5, each 4.5; the slips are sums, 12 and 13, and their lines name the two months. The tied pair is neither of the lesson's. The low and high slips are the tie rule's own two mistakes, so the likeness is the task and not the text.
- Exam `e-kruskal-h`: "Tied values share the average of their ranks." Set part 1: "Tied absolute values share the average of their ranks." One rule sentence in an instruction, as l10 S7 states it ("tied values share the average of the ranks they span"); the items share nothing else (a coding item on brokers' slippages). Not a finding.

Others. `h-mw-z` is a continuity-corrected $z$ for $U$ with a "divided by the variance" slip (0.1483); part 3 is an uncorrected $z$ for $W^+$ with slips of its own values. `h-u-moments` derives $U$'s moments without replacement; part 2 is told the formulas and its explain gives the coin argument, which no lesson gives for $W^+$. `p-two-looks` and `p-five-weeks-flip` are a sign test and a sign-flip count on other data. `e-sign-test-ties` drops ties in a sign test; `e-walsh-median` shares only $n(n + 1)/2$ as a count.

Numbers. 12.5 (as a rank sum), 92.5, 52.5, 253.75, 253.625, 15.9295, 31.8591, 1015, 2.511 and 0.99398 appear nowhere else in the course or in `topic-2.6.json`. No text field of another course file or of the exam holds six of the thirteen distinct sizes. 105 is also l10's $R_B$ and the exam's SSW in `e-algo-f`: the arithmetic of 14, no shared set. Story: "hedging error" and "hedge ratio" by two methods occur in no other stat-models file; `l13` screen 10 hedges a stock with the index by beta, another task.

## Verified, no finding

- Data and rank sum. Fourteen values in the prose, none zero, two positive (1.1, 1.9), twelve negative. Ranked by counting (not `rankdata`): sizes run 0.3, 0.6, 0.8, 1.1, 1.1, 1.4, 1.7, 1.9, ... 4.4 as the explain prints; one tie only, the positive 1.1 with the $-1.1$, at places 4 and 5; 1.9 ranks 8. $W^+ = 12.5$, $W^- = 92.5$, total 105. Slips $4 + 8 = 12$ and $5 + 8 = 13$ are as their lines say.
- Tie handling. The tie is across signs, so the rule changes $W^+$ (12 or 13 without it) and the part does test it. The question states the rule.
- Null SD with the tie. Listing all 16,384 sign patterns: untied ranks give mean 52.5 and variance 253.75, the formula's value and $1015/4$; the tied ranks give mean 52.5 and variance 253.625 ($253.75 - 6/48$), SD 15.9256. The stem says "ignoring the tie", so the key 15.9295 is the stated quantity. With the tied SD, $z = -2.5117$ and $p = 0.00601$: both sit inside the keys' bands of parts 3 and 4, so "ignoring the tie" costs nothing downstream. The tied SD itself (15.9256) is refused in part 2, rightly, since the form asked is the untied formula at 4 places.
- Part 2 claim. "Each rank $r$ joins $W^+$ with chance one half, so it adds $r^2/4$": a Bernoulli half times $r$ has variance $r^2/4$, and the ranks' signs are independent. `six-divisor` is $\sqrt{1015} = 31.8591$, the sum of squares $n(n + 1)(2n + 1)/6$ unhalved.
- Part 3. $(12.5 - 52.5)/15.9295 = -2.51106$; slips $+2.511$, $-40/253.75 = -0.1576$, $12.5/15.9295 = 0.7847$.
- Part 4, source. $\Phi(2.511) = 0.993981$ by `erfc` and by a Simpson integral, so the told 0.99398 is right to 5 places. $1 - 0.99398 = 0.00602$, doubled 0.01204, upper 0.99398 to 4 places 0.9940. A table at $z = 2.51$ gives 0.0060 as well.
- The 1% claim. Normal $p = 0.0060$; exact one-sided $p$ with the tied ranks is 73 of 16,384, 0.0045. Both under 1%, and the normal value is the cautious one.
- Bands. Each key band takes the part's printed working and the full-precision value (part 3: $-2.51106$ and $-2.511$; part 4: 0.00602, 0.0060, and 0.00604 from $z = -2.51$). Each `wrong` value is refused by its key, takes its own recomputed value, and no two bands meet. No key or slip is within 0.01 of a unit of a rounding tie at its stated places (nearest: $-0.15764$ at 3 places and 31.85907 at 4).
- Units. No part is a percentage; none carries a unit.
- Leftovers. No 8.5, 69.5, 162.5, 12.7475, 2.393, 0.0084, 0.99164, 78, 650 or "12 months" remains in the problem.
- Fix pass AF findings 6 and 7 survive the re-author: the `upper` line keeps the replacement wording and part 4 names its tail value.
- Tools on the set: validator 0 errors; voice 35 0 and 0; `fresh-check --file` 0 hits (one advisory, the bandwidth rule of `p-spread-day-tail`); `grade-all --file` 12 widgets, 0 failures. Scripts: `problems-stat-models-numbers.py` 1182 passed; `problems-stat-models-numbers-read.py` 339, 0 FINDING; `problems-stat-models-4-numbers-read.py` 153, 0; `delta-review-delta-af-stat-models-numbers.py` 558, 0; `stat-models-L3-numbers.py` 157 of 157. All exit 0.

## Engine

None. The brief's exam grep (`grep -l stat-models app/content/exams/*.json`) finds nothing, since exams name topics and `sm-` skills, not course ids; use `grep -l '"sm-'` for this course. A note for the brief, not an engine item; no inbox bullet.

## Summary

1 finding: `other` 1 (a wording slip in one explain line, exact fix above, tested). Keys changed by the fix: none. `p-hedge-ranks` is ruled `clean` on reuse and needs no further read.

## Fix pass

1. fixed by the main session: part 3 explain reads "half the rank total of 105". Delta script 0 FINDING, author script exit 0, voice 0 and 0, validator 0 errors.
