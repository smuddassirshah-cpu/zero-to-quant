# Problem sets: analysis levels 1 to 3 (brief `docs/briefs/chained.md`)

Files: `app/content/courses/analysis/problems-1.json` to `problems-3.json`. Numbers: `docs/reports/problems-analysis-numbers.py` (517 of 517 checks, exits 0).

## Sets

| set | item | parts (typed / choice) | lessons drawn on | difficulty |
|---|---|---|---|---|
| problems-1 | p-cube-root-twenty | 5 (4 / 1) | l1, l3 (and l4) | 5 |
| problems-1 | p-climbing-fractions | 5 (4 / 1) | l2, l4 | 4 |
| problems-1 | p-diagonal-fraction | 5 (4 / 1) | l5, l4 | 4 |
| problems-2 | p-sum-law-band | 5 (5 / 0) | l6, l7 | 4 |
| problems-2 | p-root-recursion | 5 (4 / 1) | l8, l6 | 5 |
| problems-2 | p-two-strands-cauchy | 5 (4 / 1) | l9, l10 | 4 |
| problems-3 | p-telescoping-tail | 5 (4 / 1) | l11, l12 | 4 |
| problems-3 | p-alternating-quarters | 5 (4 / 1) | l12, l13 | 5 |
| problems-3 | p-cube-root-greedy | 5 (4 / 1) | l12, l13, l14 | 4 |

Typed parts: 12 of 15 in each set. Every lesson of each level appears, every problem draws on two or more. Choice parts are judgements only (what a contradiction shows, which property, which test, what follows).

## Checks

1. Number script: 517 of 517, exit 0. Each numeric key is computed exactly (fractions, sympy) and by a brute search, float or mpmath run; every `wrong` value is recomputed from its named slip and shown outside the band; expression keys, accept forms and slips are tested by sympy; `numbers_lib.check_wrongs` on each set.
2. Validator: 0 errors; warnings 4522 before and after (no new warning on these files; `[key-length]`, `[tight-band]` and long-sentence warnings met while drafting were fixed).
3. Playthrough `--problems analysis/problems-<n> --local-cdn <pkgs>`: green on desktop and with `--mobile` for all three. Part screenshots at 440 px read: no overflow, fractions and sums wrap cleanly.
4. Voice scan 35 on the course folder: 0 and 0.
5. `grade-all --file` each set: 0 failures (45 widgets).

## Freshness

`fresh-check --file ... --cross-numbers`: 0 hard hits. Advisories, judged: set 1 shares the taught formula $s + \tfrac1n \in S$ with l3 (the proof step itself). Set 2: 21, 0.5714, 0.3333 with `conditional/problems-1` (coincidence: $\tfrac47$, $\tfrac13$); $|b_n - 2|$ and $|a_{n+1} - a_n|$ notation with l7 and l10. Set 3: powers of 2 (64, 256, 1024, 4096) with systems and other courses (coincidence); $|S - S_n| \le a_{n+1}$, the taught theorem.

Own-course grep (key numbers and setting of each problem, own folder first, then `app/content/`), after two rewrites:

- p-cube-root-twenty ($x^3 < 20$, 21/8, $-979$, 29.546875, 1.912109375, 16, $5q^3 = 2k^3$): 0 in analysis. First draft (cube root of 10, bisect [2, 3], left end after 3 halvings = 2.125) matched `review-1` r-bisect-sqrt3 in answer and question sentence; rewritten.
- p-climbing-fractions ($\tfrac{5n-4}{n+1}$, $\tfrac{9}{n+1}$, $\tfrac9\varepsilon - 1$, 2250): 0 in analysis. First draft used gap $\tfrac{7}{n+1}$ and threshold $\tfrac7\varepsilon$, as `exams/topic-1.10` does for $2 - \tfrac{7}{n+4}$; rewritten.
- p-diagonal-fraction (0.70329, 0.18096, 0.42571, 0.96053, 0.33418, 0.55445, 100001, 55446): 0 anywhere for the list and $x$. A draft $x = 0.5445$ matched the topic exam's diagonal slip; replaced before writing.
- p-sum-law-band ($\tfrac{6n+1}{2n+5}$, $\tfrac{2n-2}{n+1}$, 138, 80, 109, 0.09914): 0 in analysis.
- p-root-recursion ($\sqrt{4a_n + 21}$, $a_1 = 1$, $\sqrt{41}$, 6000, 14): 0 in analysis. The planned $\sqrt{3a_n + 10}$ is the topic exam's recursion; replaced before writing.
- p-two-strands-cauchy ($(-1)^n(2 - \tfrac3n)$, 3.071, 6): 0 anywhere.
- p-telescoping-tail ($\tfrac{1}{(n+1)(n+3)}$, $n^2 + 4n + 7$, 998): 0 anywhere; $\tfrac5{12}$ is common elsewhere (other courses, unrelated).
- p-alternating-quarters ($(-1)^{n+1}\tfrac{n}{4^n}$, $\tfrac5{1024}$, $\tfrac{327}{2048}$): 0 in analysis. $\sum \tfrac{n}{3^n}$ (taylor homework-3) was avoided.
- p-cube-root-greedy ($\sum \tfrac{(-1)^{n+1}}{\sqrt[3]{n}}$, $T = 0.2$, 0.2063, $-0.4237$, 0.2697): only l3's $\sqrt[3]5$ shares the symbol. $\sum \tfrac{(-1)^{n+1}}{\sqrt n}$ (l13, l14, review-3) was avoided.

Hits outside analysis (2.625, 15.45, 2250, 6.403, 0.2063 and the like) are single numbers in unrelated settings.

## Engine limits

Two bullets in `docs/BACKLOG-INBOX.md` under "Raised later (problems analysis)".
