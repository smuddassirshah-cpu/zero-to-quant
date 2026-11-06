# Stage 0 exit test extended to 0.6 and 0.7

File: `app/content/exams/stage-0.json`. Scripts: `docs/briefs/exam-stage-0-scripts/` (`build.py` route A, `check_numbers.py` route B, `fresh.py`).

## Design (written before the build)

- Source: the 0.6 bullet of the Stage 0 exit test in `docs/curriculum.md` ("five short statements proved, one each by direct proof, contrapositive, contradiction, induction and counterexample, written so a stranger can check every step") and PLAN item 8 (extend stage-0 to 0.6 and 0.7).
- Existing parts keep their ids, items and order: `gcse`, `precalc`, `zetamac`, `script`. The new paper goes third among the parts, after `precalc`, so paper indices 0 and 1 are unchanged; the two new checks go after the existing checks, so check indices 0 and 1 (the engine ticks checks by position) are unchanged.
- New paper `proof`, "Reasoning and proof", pass 0.7, 12 items on the `proof` course skills, ramp 2, 7, 2, 1 at difficulties 2 to 5:
  - five `order` proofs, one per method, each with two flawed lines (direct: $n$ odd gives $8 \mid n^2 - 1$; contrapositive: $n^3 + 5$ odd gives $n$ even; contradiction: $\log_2 5$ is irrational; induction: $3^n > n^3$ from $n = 4$; counterexample: "if $a$ divides $bc$ then $a$ divides $b$ or $c$" fails at $a = 4$, $b = c = 2$);
  - five auto-graded checks, one per method (a numeric step of the direct proof, the contrapositive of a statement, Euclid's product for the primes to 17, the induction base, the first failure of $2n^2 + 29$);
  - two on the earlier proof levels: a negation with quantifiers, and a function that is onto but not one-to-one.
- New checks: `proofs-written` (the five proofs written out for a stranger, the part the app cannot mark).
- Every number fresh against all content files (`fresh.py`) and recomputed by `check_numbers.py`, which also asserts that every old part and item id is still there, in order.

## Result

- Parts, in order: `gcse`, `precalc`, `proof` (new), `zetamac`, `script`, `proofs-written` (new). The 40 old item ids and both old papers and checks are unchanged; `check_numbers.py` compares them with a list frozen before the change. The only other edit to an old field is `description`, which names the proof paper and the written proofs (and no 0.7 plan).
- Paper `proof`, "Reasoning and proof": 45 minutes (1.25 times the summed pace), pass 0.7, 12 items, ramp 2, 7, 2, 1.
- Per method, an order proof with two flawed lines and an auto-graded check:
  - direct: $n$ odd gives $8 \mid n^2 - 1$; check $m$ at $n = 13$ (21);
  - contrapositive: $n^3 + 5$ odd gives $n$ even; check the contrapositive of "if $ab > 9$ then $a > 3$ or $b > 3$";
  - contradiction: $\log_2 5$ is irrational; check Euclid's number for the primes to 17 ($510{,}511 = 19 \times 26{,}869$, key 19);
  - induction: $3^n > n^3$ for $n \ge 4$; check the smallest such $N$ (4);
  - counterexample: "$a$ divides $bc$ gives $a$ divides $b$ or $c$" fails at $a = 4$, $b = c = 2$; check the first failure of $2n^2 + 29$ (29).
- Two more items cover proof levels 1 and 2: a negation through three quantifiers and a function onto but not one-to-one.
- Each order item's `byKey` carries a line per flawed line and a `left-out` line. The induction order item has `same: [[i3, i4]]` and the direct proof `same: [[o2, o3]]`, so either order of those independent lines is accepted.

## Gates

- Validator: 0 errors. Warnings on `stage-0.json`: one, `parts[1].items[1].widget.wrong[0]` `[O2-no-slip]`, on the old precalc item `p-index`. It predates this change, and old items are left as they are.
- Voice scan on a copy: 0 sentences over 20 words, 0 explanations over three sentences, 659 sentences.
- `check_numbers.py`: 108 of 108, exit 0. Route B: each proof's algebra over a range of integers, a brute-force search for the counterexample triple, a sieve for the $2n^2 + 29$ search, trial division for Euclid's number, a direct search for the induction base, a grid for the contrapositive, $\ln 5 / \ln 2$ for the printed digits, and the number pass over every new string.
- Playthrough with `--local-cdn`: green with and without `--mobile`.
- `readiness-sums.mjs`: OK.
- Second-reader fix pass (`docs/reviews/review-exam-stage-1.md`): the 0.7 description line, the `same` sets, the item 1 prose and tolerances, braced thousands commas in maths, two option changes (long keys, learner-action whys), and fresh contrapositive and counterexample setups.

## Freshness

`fresh.py` finds none of the statements in any other file. The proof course uses Euclid's 30,031 in l12, $2^n > n^2$ in l13 and homework 3, $3n + 1$ in l11, and $n^2 + n + 41$ and "$2^p - 1$ is prime for every prime $p$" in l14. The fix pass replaced the contrapositive and counterexample setups, which were those lessons' families with new constants, with $n^3 + 5$ and a divisibility claim found in no content file; `fresh-check.mjs --exam stage-0` has no hit on either beyond the shared frame "put the proof in order". Shared numbers (168) are common values in unrelated items.

## Note for the main session

- `curriculum.json` stage 0 `exitTests` still omits the 0.6 line; it is not edited here.
- Session U orchestrator: `getting-hired` was removed after the build, because `docs/curriculum.md` line 91 says 0.7 is not part of the exit test and a check gates the pass. PLAN item 8 is met for 0.6; 0.7 stays outside the exit test.
