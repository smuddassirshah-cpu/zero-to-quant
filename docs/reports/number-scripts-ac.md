# Number scripts repaired after the AC content passes

Method: all 309 `docs/reports/*-numbers.py` and the 51 `*number*.py` under `docs/briefs/*-scripts/` and `docs/reviews/*-scripts/` (360 scripts) were run at the branch tip (timeout 100 s, `xargs -P 4`), then every failure was re-run in the checkout of 3243731. Scripts not named `*number*` in those folders were not run.

## Counts

- Run: 360.
- Failing at the tip before repair: 44 (9 of them timeouts at 100 s).
- Failing at 3243731 too (not mine): 28 (list below).
- Broken today: 16. Repaired: 15. Still failing: 1 (`bank-2-s2-numbers.py`, two content findings, below).
- Failing now: 29 (28 older plus `bank-2-s2`).

## Repaired (15)

Method for `sign`, `sign2`, `decimal`: a small `derived_slips()` helper in each script adds, for every `wrong` id of the form `sign`, `sign<n>` the absolute value of the key the script computes, and for `decimal` that key over 100 (over 10,000 where the part text holds `%²`). The existing checks then compare the value with the content inside its tolerance and require it to lie outside the key band, so a sign entry on a non-negative key fails. Ids the script already had in its slips are untouched. No assertion was deleted or loosened.

- `docs/reports/problems-{conditional,counting,estimation,limits-thm,markov,random-vars,taylor,trig,vectors}-numbers.py`: helper as above (trig inside `wrong_checks`, with the computed key passed in).
- `docs/reports/problems-integrals-numbers.py`, `problems-multivar-numbers.py`: helper in the numeric `num()`.
- `docs/reports/bank-2-s1-numbers.py`: helper in `numeric()` (`pf-types-round-half-even`).
- `docs/briefs/exam-stage-1-scripts/check_numbers.py`: `d-residue` and `d-damped-value` `sign` asserted as the absolute value of the computed key (key negative asserted); the `sign` byKey line states cos 3 = -0.9900 and (2/3) sin 3 = 0.0941, now allowed from `math.cos(3)` and `2/3*math.sin(3)`, with the closed form e^-2 (cos 3 + (2/3) sin 3) checked against the integration.
- `docs/briefs/exam-1.10-scripts/check_numbers.py`: `e-ftc-both-limits` `sign` = |F'(2)| = 1/65 (key negative asserted, 1/5 - 12/65 = 1/65 checked); the byKey line's 13 (13/65) allowed.
- `docs/briefs/exam-stage-3-scripts/check_numbers.py`: part C text additions: `r-t-bar` "2.76" recomputed as 0.45 / 0.163 = 2.7607 and checked inside the widened band; `r-best-of-twenty` "0.22" recomputed as 1 - 0.9875^20 = 0.2224 (and 1 - 0.775 = 0.225), inside the band.
- `docs/reports/bank-2-s2-numbers.py` (partly): the `ds-pointers-merge-ticks` checks were updated for fix pass delta AC-2, which added the old no-shared-time test back as test 11: "stale value gone" now allows that setting in test 11 only (and asserts it is test 11), and the count asserts 11.

Part D (10 slips merged or narrowed): no script of the 16 depended on it; none was broken by it.

## Content findings (script left failing)

1. `app/content/bank/statistics-2.json` item `es-intervals-poll-margin`, `wrong` entry `decimal`: value 0.04801 (key 4.801 over 100, correct) with `tol.abs` 0.05. The band is wider than the value (accepts 0 to 0.098), and the script's existing rule "band not over half the value" fails. The tolerance was copied from a neighbour; it should be about 0.0005 or less (the key's own tol is 0.04, so 0.0004 keeps the same relative width). Value not in dispute.
2. `app/content/bank/coding-2.json` item `ds-pointers-merge-ticks`: 11 hidden tests after the delta AC-2 fix pass; the shared check `docs/reports/bank_2_code_check.py` and `docs/briefs/bank-2.md` rule 12 require six to ten. Either the brief limit is relaxed or test 11 is merged. Not a sign/decimal matter.

## Older failures (also failing at 3243731, not touched)

Timeouts at 100 s in both: `bank-2-s3`, `coding-int-3-perf`, `coint-1-perf`, `coint-L1`, `fluency-exp-log`, `fluency-integrals`, `fluency-odes`, `fluency-quadratics`, `problems-limits` (all `docs/reports/*-numbers.py`). `bank-2-s3` covers files not changed today, so it cannot have broken.

Non-zero exit in both: `docs/briefs/coding-int-scripts/numbers_fix.py`, `docs/briefs/exam-stage-2-scripts/check_numbers.py`, `docs/reports/numerics-L3-numbers.py`, `docs/reports/py-found-L1..L4-numbers.py`, `docs/reviews/exam-0.1-scripts/numbers.py`, `exam-0.2-scripts/numbers.py`, `exam-1.1-scripts/numbers.py`, `exam-1.2-scripts/numbers.py`, `exam-mock-oa-sig-versions-scripts/read_numbers.py`, `number-sense-4-scripts/dump.py`, `number-sense-4-scripts/read-numbers.py`, `quadratics-4-scripts/read-numbers.py`, `review-problems-number-sense-1-3-scripts/show.py` and `taught.py`, `stat-learning-4-scripts/read-numbers.py`, `testing-4-scripts/read-numbers.py`. Many of these are dump or reader scripts that depend on state outside the repo.

## Notes

- The fix pass AC-2 also changed content (bank tests); its author did not run the bank scripts. Authors of later passes should run the author scripts of the course they touch.
