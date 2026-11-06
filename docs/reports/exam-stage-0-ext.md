# Stage 0 exit test extended to 0.6 and 0.7

File: `app/content/exams/stage-0.json`. Scripts: `docs/briefs/exam-stage-0-scripts/` (`build.py` route A, `check_numbers.py` route B, `fresh.py`).

## Design (written before the build)

- Source: the 0.6 bullet of the Stage 0 exit test in `docs/curriculum.md` ("five short statements proved, one each by direct proof, contrapositive, contradiction, induction and counterexample, written so a stranger can check every step") and PLAN item 8 (extend stage-0 to 0.6 and 0.7).
- Existing parts keep their ids, items and order: `gcse`, `precalc`, `zetamac`, `script`. The new paper goes third among the parts, after `precalc`, so paper indices 0 and 1 are unchanged; the two new checks go after the existing checks, so check indices 0 and 1 (the engine ticks checks by position) are unchanged.
- New paper `proof`, "Reasoning and proof", pass 0.7, 12 items on the `proof` course skills, ramp 2, 7, 2, 1 at difficulties 2 to 5:
  - five `order` proofs, one per method, each with two flawed lines (direct: $n$ odd gives $8 \mid n^2 - 1$; contrapositive: $5n + 7$ even gives $n$ odd; contradiction: $\log_2 5$ is irrational; induction: $3^n > n^3$ from $n = 4$; counterexample: $n^2 + n + 17$ fails at $n = 16$);
  - five auto-graded checks, one per method (a numeric step of the direct proof, the contrapositive of a statement, Euclid's product for the primes to 17, the induction base, the first failure of $2n^2 + 29$);
  - two on the earlier proof levels: a negation with quantifiers, and a function that is onto but not one-to-one.
- New checks: `proofs-written` (the five proofs written out for a stranger, the part the app cannot mark).
- Every number fresh against all content files (`fresh.py`) and recomputed by `check_numbers.py`, which also asserts that every old part and item id is still there, in order.

## Result

- Parts, in order: `gcse`, `precalc`, `proof` (new), `zetamac`, `script`, `proofs-written` (new). The 40 old item ids and both old papers and checks are unchanged; `check_numbers.py` compares them with a list frozen before the change. The only other edit to an old field is `description`, which now names the proof paper and the new check.
- Paper `proof`, "Reasoning and proof": 45 minutes (1.25 times the summed pace), pass 0.7, 12 items, ramp 2, 7, 2, 1.
- Per method, an order proof with two flawed lines and an auto-graded check:
  - direct: $n$ odd gives $8 \mid n^2 - 1$; check $m$ at $n = 13$ (21);
  - contrapositive: $5n + 7$ even gives $n$ odd; check the contrapositive of "if $ab > 9$ then $a > 3$ or $b > 3$";
  - contradiction: $\log_2 5$ is irrational; check Euclid's number for the primes to 17 ($510{,}511 = 19 \times 26{,}869$, key 19);
  - induction: $3^n > n^3$ for $n \ge 4$; check the smallest such $N$ (4);
  - counterexample: $n^2 + n + 17$ fails at $n = 16$; check the first failure of $2n^2 + 29$ (29).
- Two more items cover proof levels 1 and 2: a negation through three quantifiers and a function onto but not one-to-one.
- Each order item's `byKey` carries a line per flawed line and a `left-out` line.

## Gates

- Validator: 0 errors. Warnings on `stage-0.json`: one, `parts[1].items[1].widget.wrong[0]` `[O2-no-slip]`, on the old precalc item `p-index`. It predates this change, and old items are left as they are.
- Voice scan on a copy: 0 sentences over 20 words, 0 explanations over three sentences, 659 sentences.
- `check_numbers.py`: 103 of 103, exit 0. Route B: each proof's algebra over a range of integers, a sieve for the two counterexample searches, trial division for Euclid's number, a direct search for the induction base, a grid for the contrapositive, $\ln 5 / \ln 2$ for the printed digits, and the number pass over every new string.
- Playthrough with `--local-cdn`: green with and without `--mobile`.
- `readiness-sums.mjs`: FAIL on the catalogue block only, as in `docs/reports/exam-stage-1.md`; no exam file moves it.

## Freshness

`fresh.py` finds none of the statements in any other file. The proof course uses Euclid's 30,031 in l12, $2^n > n^2$ in l13 and homework 3, $7n + 4$ in l11, and $n^2 - n + 11$ in homework 3. Each was avoided before the first build. Shared numbers (168, 289) are common values in unrelated items.

## Note for the main session

- `docs/curriculum.md` line 91 says 0.7 is not part of the exit test, but PLAN item 8 asked for it. The engine passes a stage exam only when every check is ticked, so `getting-hired` now gates the Stage 0 pass. If 0.7 should stay outside the pass, drop that check, or let the engine mark a check optional (backlog bullet).
- `curriculum.json` stage 0 `exitTests` still omits the 0.6 line; it is not edited here.

- Session U orchestrator: `getting-hired` removed after the build, because `docs/curriculum.md` line 91 says 0.7 is not part of the exit test and a check gates the pass. PLAN item 8 is met for 0.6; 0.7 stays outside the exit test.
