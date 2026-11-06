# Algebra levels 3 and 4: second-reader findings

Scope: `app/content/courses/algebra/` lessons l10 to l17, `review-3.json`, `review-4.json`, `homework-3.json`, `homework-4.json`. Levels 1 and 2 are not in this tree and were not read.
Method: every stated number and every wrong-option value recomputed in a scratch script (Python: modular arithmetic, a D4 model as pairs r^a s^m checked against the brief's matrices, brute-force subgroup and normality search, polynomial products and long division over Q and Z_p, XOR CRC, brute-force irreducible counts). Every Cayley table, coset shade set, power grid, Z_7, Z_6, Z_4 and F_4 table was checked cell by cell (421 checks, all passed except the items below). Each code widget was run in CPython: solution against tests and examples, starter against tests. Each distractor `why` and `byKey` line was read against the learner action it names, and against what `table.js` and `player.js` actually return as the key.

## Automated checks

- `python3 docs/reports/algebra-L3-numbers.py`: exit 0, numbers_lib 146 of 146, 3 code widgets (solution passes, starter fails), 9 "check by hand" lines. I checked all nine by hand: each byKey names its wrong value correctly.
- `python3 docs/reports/algebra-L4-numbers.py`: exit 0, numbers_lib 83 of 83, 3 code widgets, 8 "check by hand" lines, all correct by hand.
- Stated numbers the scripts do not check: that the l13 RSA `cube` value matches its slip (only its tolerance is checked; finding 1); the l16 trap remainder for `q = x` (finding 2); how many SEDOL positions share a weight (finding 3); the l17 hook's start-point heights -1.875, 0.375 and 1.875 (correct by my computation); homework-4 `sqrt(221) ≈ 14.9` (correct); the Z_9 claim in l15 quiz[1] (finding 5).
- `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors, 2282 warnings course-wide. On these files: five "ladder reuses the previous canvas kind" warnings (l10 s3, l11 s3, l12 s3, l13 s6, l14 s6), plus the unwritten-lessons and locked-level-3 notices. `content/manifest.json` was restored afterwards.
- `VOICE_BASE=app/content/courses/algebra python3 docs/reviews/voice-scan.py`: explanations over three sentences 0; sentences over 20 words 0.
- My own scan: no exclamation marks, no em or en dashes, no American spellings. All 6 code solutions pass every test and example. Each starter fails at least one test: l10 fails 5 of 10, l13 7 of 10, l16 4 of 8, l17 4 of 9, homework-3 6 of 6, homework-4 3 of 8.

## Findings

Severity: wrong = a false statement or a wrong value; misleading = true but steers the learner wrongly, or feedback that never fires; voice = AUTHORING section 6; layout = canvas, highlight or structure.

1. **wrong**. `l13-fermat-and-euler.json` `screens[9].widget.rows[1][1].wrong[0]` (id `cube`, value 31), with `feedback.byKey.r1c1`.
   Problem: the line for this cell is "You raised 31 to the public exponent again". But $31^3 \bmod 33 = 25$, not 31. The value 31 is the slip "copied the ciphertext". Also, because of finding 4, the line never fires for 31.
   Evidence: `pow(31, 3, 33) == 25`.
   Fix: set `wrong` to `[{ "id": "cube", "value": 25 }, { "id": "copy", "value": 31 }]`. Set `byKey.cube` to "You raised 31 to the public exponent 3, which gives 25. Decryption uses the private exponent 7." Set `byKey.copy` to "You copied the ciphertext. Raise 31 to the private exponent 7 and reduce mod 33." Delete `byKey.r1c1`.

2. **wrong**. `l16-polynomials.json` `screens[8].widget.options[3].why` (id `round`).
   Problem: "With $q = x$ the remainder is $-x + 1$, of degree 1, not below 1." In fact $x^2 + 1 - x(2x + 1) = -x^2 - x + 1$, of degree 2.
   Fix: "With $q = x$ the remainder is $-x^2 - x + 1$, of degree 2, not below 1."

3. **wrong**. `l10-homomorphisms.json` `quiz[0].widget.options[2].why` (id `diff`).
   Problem: it says "two positions share weight 1". The weights are 1, 3, 1, 7, 3, 9, 1, so three positions have weight 1.
   Fix: "You looked for distinct weights, but three positions share weight 1 and two share 3. Each weight on its own matters."

4. **misleading**. Table widgets in both levels: each cell's `wrong[]` slip is dead, and the line meant for that slip fires on other wrong answers.
   Problem: `table.js` `grade()` returns the matching `wrong[].id` as the key, and the cell id (`r0c1`) only when no `wrong` entry matches. `player.js` `notYetLine` uses `byKey[key]` and otherwise falls back to the generic line. Every byKey line below is keyed on the cell id but names the cell's own `wrong` value. So typing the named slip (12 for $3 \times 4$) gives the generic line. Any other wrong number in that cell gives "You wrote 12 for $x = 4$". The brief told the author to key on the cell id, but that workaround is stale: ENGINE-BACKLOG 576 (done) makes `validate.mjs` accept a cell's `wrong` ids as keys.
   Fix: rename each key from the cell id to the `wrong` id and keep the text. Add a line for each `wrong` id that has none:
   - `l11-normal-subgroups.json` `screens[5]`: rename `byKey.r1c1` to `r2` and copy it to `r2b` and `r2c`, as "You typed $r^2$. That is right as an element, but $r^2 \in N$, so the coset is $eN$." Also add `"accept": ["N"]` to `widget.rows[0][1]`, as rows 1 to 3 already have it.
   - `l12-first-isomorphism-theorem.json` `screens[0]`: rename `byKey.r0c1` to `unreduced4`. Give `unreduced5` to `unreduced11` each "You wrote $3x$ before reducing. Take away 12 until the value is below 12."
   - `l13-fermat-and-euler.json` `screens[0]`: rename `byKey.r2c1` to `raw3`. Give `raw4`, `raw5` and `raw6` each "You wrote $2^k$ before reducing. Take away multiples of 7 to land in 0 to 6."
   - `l13-fermat-and-euler.json` `screens[6]`: rename `r0c1` to `nminus1`, `r1c1` to `nminus1b` and `r2c1` to `raw`.
   - `l13-fermat-and-euler.json` `screens[9]`: rename `r0c1` to `raw64`. For `r1c1`, see finding 1.
   - `l14-rings.json` `screens[1]`: rename `r0c1` to `raw6` and `r1c1` to `raw11`.
   - `l15-fields.json` `screens[1]`: rename `r2c1` to `neg`.
   - `l15-fields.json` `screens[9]`: rename `r0c1` to `slope` and `r1c1` to `half`.
   - `l16-polynomials.json` `screens[4]`: rename `r0c1` to `raw2` and `r1c1` to `raw1`.
   - `l16-polynomials.json` `screens[7]`: rename `r0c1` to `half`.
   - `l17-roots-and-factors.json` `screens[6]`: rename `r0c1` to `double`.
   - `homework-4.json` `items[2]`: rename `r0c1` to `half` and `r4c1` to `neg`.
   Then run the validator to confirm the new keys are accepted (item 576).

5. **misleading**. `l15-fields.json` `quiz[1].widget.options[3].why` (id `odd`).
   Problem: "$\mathbb{Z}_9$ is odd and also fails, since $3 \times 3 = 0$." With the lesson's shares at $x = 1, 2, 3$, every difference of $x$ values (1 or 2) is a unit mod 9. So two-share recovery works over $\mathbb{Z}_9$ there. It fails only when two $x$ values differ by a multiple of 3.
   Fix: "Parity is not the point. Over $\mathbb{Z}_9$, shares at $x = 1$ and $x = 4$ fail too, since 3 has no inverse."

6. **misleading**. `l15-fields.json` `screens[6].widget.options[7]` (id `n1`, text "1").
   Problem: the question asks about "$n$ from 2 to 12", but one option is 1, outside that range. A learner who reads the range cannot treat it as a candidate.
   Fix: change `question` to "For which $n$ from 1 to 12 is $\mathbb{Z}_n$ a field? Select all that apply." Keep the option and its `why`.

7. **misleading**. `homework-3.json` `items[7].explain.text`, third sentence.
   Problem: "For $d = 4$, $n = 10$ there is no subgroup $\langle 4 \rangle$ of index 4". But $\langle 4 \rangle$ exists in $\mathbb{Z}_{10}$: it is $\{0, 2, 4, 6, 8\} = \langle 2 \rangle$, of index 2. The sentence suggests the subgroup is missing.
   Fix: "In $\mathbb{Z}_{10}$, $\langle 4 \rangle = \langle 2 \rangle$ has index 2, not 4, so the call raises."

8. **misleading**. `l14-rings.json` `screens[5].widget.lines[3]` (id `u4`).
   Problem: the line cites "$x0 = 0$", but screen 3 proved only $0a = 0$. The mirror needs the other distributive law, and no screen states it.
   Fix: "$a^{-1}(ab) = a^{-1}0 = 0$ (assumption; $x0 = 0$ as for $0a$, by the other distributive law)."

9. **misleading**. `l10-homomorphisms.json` `screens[10].prose`.
   Problem: "Swapping neighbours $a, b$ changes the sum by $(w_1 - w_2)(a - b)$." New minus old is $(w_1 - w_2)(b - a)$, so the stated sign is wrong. It does not matter for the mod-10 test, but the statement is false as written.
   Fix: replace "$(w_1 - w_2)(a - b)$" with "$(w_1 - w_2)(b - a)$". The canvas row of $w_1 - w_2$ stays as it is.

10. **layout**. Hint highlights that point at the wrong cell:
    - `l11-normal-subgroups.json` `screens[2].hints[1].highlight` `["r3c2"]` is row $r$, column $s$, the product $rs$. The hint is about $sr^3 = rs$, which is row $s$, column $r^3$: `r2c7` in this coset-ordered grid. Fix: `["r2c7"]`.
    - `l13-fermat-and-euler.json` `screens[2].hints[1].highlight` `["col6"]` goes with the text "Row 2 first reaches 1 at $k = 3$". Fix: `["r2c3"]`.
    - `l14-rings.json` `screens[6].hints[1].highlight` `["Z"]` lights the zero matrix while the text is "$\mathbb{Z}_{12}$ has $3 \times 4 = 0$". Fix: delete `hints[1].highlight` and add `"highlight": ["A", "B", "Z"]` to `hints[2]`, whose text is about the matrices.

11. **voice**. Multi distractors whose `why` states a computation but names no learner action (AUTHORING section 6):
    - `l14-rings.json` `screens[2].widget.options[4].why` (`x0`): "You may have read the factors' product 6 as zero" names no natural slip. Fix: "You may have taken 0 as a root, as for $x^2 - 5x$. At $x = 0$ the value is the constant term 6."
    - The same pattern appears in `l14-rings.json` `screens[2]` options `x8`, `x9` and `quiz[1]` options `i3`, `i6`, `i8`; `l15-fields.json` `screens[6]` options `n9`, `n4`; and `l17-roots-and-factors.json` `screens[4]` options `x2`, `x4`, `x6`. Fix: start each `why` with the action, for example `x8`: "You kept 8. There the factors are 6 and 5, with product $30 \equiv 6$." Use the same form for the others ("You kept 9.", "You kept 3.").

12. **voice**. `l14-rings.json` `screens[2].prose` is 62 words, against a limit of 60 (AUTHORING section 2).
    Fix: replace the first two sentences with "A **ring** is an abelian group under $+$ with an associative $\times$ that has a unity 1 and distributes over $+$."

13. **voice**. `l16-polynomials.json` `screens[7].hints[2].text`: "then x + 1 ÷ 2x gives 3" is plain text with no brackets, and it reads as $x + \tfrac{1}{2x}$.
    Fix: "Next $2x^2 \div 2x = x$, then $(x + 1) \div 2x$ gives 3, leaving $1 - 3 = -2 \equiv 3$."

14. **voice**. `l13-fermat-and-euler.json` `screens[0].prose`: "Each power is the one before times 2, reduced mod 7" reads as true of every row, but it holds only for base 2.
    Fix: "In row 2, each power is the one before times 2, reduced mod 7."

15. **layout** (brief conformance). `homework-3.json` `items[6]` (`h-power-in-n`).
    Problem: the brief asks for an `order` item proving Euler's theorem from Lagrange's, or that the coset product is well defined. The item instead proves $g^m \in N$ for $|G/N| = m$. Both named proofs are already graded in the lessons (l13 s5, l11 s8). The new item is a sound Pinter chapter 15 exercise, and it is correct.
    Fix: keep it, and record the substitution in DECISIONS (my recommendation). Otherwise replace it with the Euler `order`.

## Counts

15 findings: wrong 3, misleading 6, voice 4, layout 2. Numbers: every stated value in both levels is right except the three in findings 1 to 3.

## Engine item for the inbox

- `tools/validate.mjs`, `table` widget: warn when an editable cell has `wrong[]` ids with no `byKey` line, and above all when `byKey` is keyed on that cell's id. In that case the cell-id line can never fire for the slip it names (finding 4: 13 screens in these two levels). The old workaround in the briefs and inbox bullets (key on `r{i}c{j}`) predates item 576. Other courses written under it probably have the same dead lines, so a course-wide scan is worth running. `docs/briefs/algebra.md` ("Known limits already in the inbox") still tells authors to key on the cell id, and needs the same correction.

## Fix pass

1. fixed: l13 s9 `cube` slip is now 25 (31^3 mod 33 = 25, recomputed), new `copy` slip 31, lines keyed `cube` and `copy`, `r1c1` removed.
2. fixed: l16 s8 `round` why now reads $-x^2 - x + 1$, degree 2 (x^2 + 1 - x(2x + 1) = -x^2 - x + 1).
3. fixed: l10 quiz[0] `diff` why says three positions share weight 1 (weights 1, 3, 1, 7, 3, 9, 1).
4. fixed: all 12 listed table screens (the review says 13, its list has 12) re-keyed from cell id to wrong id; l11 s5 `r2`, `r2b`, `r2c` share one line and `accept: ["N"]` added to row 0; l12 s0 `unreduced5` to `unreduced11` and l13 s0 `raw4` to `raw6` get new lines. Validator accepts the keys. `docs/briefs/algebra.md` corrected (ENGINE-BACKLOG 576).
5. fixed: l15 quiz[1] `odd` why now names shares at x = 1 and x = 4 (difference 3, no inverse mod 9).
6. fixed: l15 s6 question now "from 1 to 12".
7. fixed: homework-3 items[7] explain: $\langle 4 \rangle = \langle 2 \rangle$ has index 2 in $\mathbb{Z}_{10}$.
8. fixed: l14 s5 `u4` line cites the other distributive law.
9. fixed: l10 s10 prose now $(w_1 - w_2)(b - a)$. The generic line on that screen keeps $(a - b)$, where the sign does not affect the multiple-of-10 test.
10. fixed: l11 s2 hint to `r2c7`, l13 s2 hint to `r2c3`; l14 s6 hint[1] highlight removed and `["A", "B", "Z"]` moved to hint[2]. This leaves one validator warning (point hint without highlight) on l14 s6, accepted because the canvas holds only matrices.
11. fixed: `why` lines of l14 s2 `x0`, `x8`, `x9`, l14 quiz[1] `i3`, `i6`, `i8`, l15 s6 `n9`, `n4`, l17 s4 `x2`, `x4`, `x6` now start with the action ("You kept ...").
12. fixed: l14 s2 prose now 60 words by whitespace count.
13. fixed: l16 s7 hint[2] bracketed $(x + 1) \div 2x$.
14. fixed: l13 s0 prose says "In row 2, each power ...".
15. deferred: keep the `h-power-in-n` item; recording the substitution in DECISIONS is outside this fix scope (algebra L3 and L4 files only).

Counts: fixed 14, disputed 0, deferred 1. Graded answers changed: 0 (l11 row 0 now also accepts N).
Engine note: not actioned here (engine item for the inbox).
Number scripts: `algebra-L3-numbers.py` (151 of 151) and `algebra-L4-numbers.py` (85 of 85) updated with the cube and copy slips, the `byKey.raw` path, the SEDOL weight count, the trap remainder and the Z_9 claim; both exit 0.
Gates: validator 0 errors; voice scan 0 and 0; playthrough green with and without `--mobile` for l10 to l17, homework-3 and homework-4 (review-3 and review-4 unchanged).
