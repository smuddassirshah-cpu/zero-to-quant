# Engine pass AC part 2: fast test-validate-* files

## What changed

- `app/tools/validate.mjs`: a `--root <dir>` option (root handling only, no rule). The folder above `<dir>` plays the part of `app/` for the files
  that sit beside content: `tools/fixtures/problems`, `tools/fixtures/fluency`, `tools/perf-pending.json`, and the `docs/reports` number-script
  lookup. Report paths read `content/...` either way. `--no-manifest` already existed; a `--root` run without it writes `<dir>/manifest.json`
  (the scratch copy), never `app/content/manifest.json`. `fluency-rules.mjs` `fixtureFiles(dir)` takes the folder as an optional argument
  (same default).
- `app/tools/fixtures/mini-app/` (1.1 MB, 42 files, README inside): a cut-down copy of the real content laid out like `app/`. Validates with
  0 errors in 0.4 s (real root: 16.7 s). It carries 64 warnings, all inherited from the real lessons it holds (not-yet-written, O2 voice notes,
  key-length); no case asserts on "no warnings".
- `app/tools/lib/validate-harness.mjs`: `openHarness({ name, fixtures })` copies the mini root to a temp folder, `h.validate(args)` runs the real
  `validate.mjs --root` on it and returns `{ out, code, errors, warnings }`. `ZQ_VALIDATE=<file>` points it at a mutated validator (used below).
- 14 of the validator-running test files ported; `test-validate-near-miss` and `test-validate-versions` ported with small edits (below).
  `test-validate-o2`, `-perf`, `-capstone` never ran the validator (they call the rule libraries on fixtures, 0.1 s each) and are untouched.
- New `app/tools/test-validate-harness.mjs` (7 checks): mini root 0 errors alone and beside the real fixtures, planted-into files exist,
  `--root` never touches `app/content/manifest.json`.
- `census`, `fresh-check`, `grade-regression` and the playthrough read `app/content` only, so `tools/fixtures/mini-app` is invisible to them
  (grade-regression also has its explicit `tools/fixtures` skip).

## Table (16 validator-running files, plus the three library files)

Before = the old file on the real root. Measured where it fits in two minutes (M), otherwise 12 s copy + runs x 16.7 s (E, a lower bound: the old
session file also ran the validator once per candidate lesson while looking for its target). Cases = PASS lines, identical before and after (the
diff of every file is only its setup lines; see "No check dropped").

| file | cases | validator runs | before | after |
|---|---|---|---|---|
| answer-forms | 24 | 24 | 413 s E | 10.7 s |
| band-rules | 40 (41 with --local-cdn) | 1 (2) | 29 s E | 0.6 s (2 s with cdn) |
| drill-index | 8 | 8 | 146 s E | 4.1 s |
| fluency | 43 | 45 | 764 s E | 27.9 s |
| near-miss | 9 | 1 | 29 s E | 0.5 s |
| problems | 42 | 44 | 747 s E | 15.5 s |
| review-pass | 2 | 2 | 42 s M | 0.8 s |
| session-v-b | 32 | 32 | 546 s E | 11.7 s |
| session | 32 | 17 | 296+ s E | 5.8 s |
| shown-arithmetic | 8 | 8 | 146 s E | 2.8 s |
| shuffled-position | 13 | 13 | 229 s E | 5.1 s |
| table-slip-key | 4 | 4 | 80 s M | 1.9 s |
| table-wrong | 3 | 3 | 65 s M | 1.1 s |
| versions | 5 (+summary) | 5 | 95 s E | 1.9 s |
| why | 12 | 13 | 229 s E | 5.9 s |
| wrong-fire | 5 | 5 | 118 s M | 2.9 s |
| o2, perf, capstone | 6, 36, 17 | 0 | 0.1 s each | 0.1 s each |
| harness (new) | 7 | 3 | n/a | 3.1 s |

Total: about 3950 s (66 min) before, about 102 s after, run one file at a time. The slowest file is fluency at 28 s. Each file is one process, so
two cores make no difference; the whole set is far under 5 minutes either way. Of the old files, only review-pass, table-wrong, table-slip-key
and wrong-fire finished inside two minutes; all four passed (2, 3, 4 and 5 PASS lines), matching the new runs. The seven files not confirmed
green last session (fluency, problems, session, session-v-b and three more) all pass now: 43, 42, 32 and 32 cases, 0 FAIL.

## Cases kept on the real root

None. Every case ran on the mini root. Two behaviour notes, neither a weakened assertion:
- `test-validate-session` finds its target lesson by scanning for the first lesson with no stated duration; on the mini root that is
  `algo-think/l1-counting-work` (before: the first such lesson of the real tree). The 17 cases and their assertions are unchanged.
  It reads `tools/duration-prose-ignore.json` from the real tools folder (the validator reads that same file).
- `test-validate-versions` no longer runs `apply-item6-content.mjs` in its copy: that script only writes the `versionOf` fields and the
  mock-oa-code text into the real exams, and the mini root's exams already carry them. The 5 cases are unchanged.
- `test-validate-near-miss` still calls `planted-check.mjs` with `ZQ_APP_DIR` set to the scratch folder (which holds `content/drills`).

## No check dropped

`git diff -U0` over the 16 ported files shows only: the `os` and `child_process` imports, the temp-folder creation, the 83 MB `cpSync`,
the `run` definition, the duration-ignore path, and header comments. No `say(`, case array row, regex or expected string changed.
Case counts match the old files' own PASS/FAIL line counts where the old file finished (4 files above) and the source rows elsewhere.
Two cases needed a fuller mini root than first built, found by running them: `problems` "skill-from-another-level" needs equations level 3
fully written (the rule only runs on a complete level), and the exam/bank cases needed `recruiting` and exam skills that exist.

## Mutation spot check (a mutated copy of validate.mjs via ZQ_VALIDATE, deleted afterwards)

| test | mutation | result |
|---|---|---|
| wrong-fire | `wrongCannotFire` returns at once | 3 of 5 FAIL (equal-to-answer, wide tolerance, overlapping) |
| table-wrong | the byKey "cannot return the key" check disabled | 1 of 3 FAIL ("unknown byKey key: still refused") |
| review-pass | the missing-`pass` error never fires | 1 of 2 FAIL ("review without pass: error") |
| shuffled-position | the `[shuffled-position]` warning disabled | 4 of 13 FAIL |
| answer-forms | the "list of two or more TeX strings" message changed | 1 of 24 FAIL |

A first wrong-fire mutation (only the `d <= ha` branch) did not fail the test: the "equal to the answer" case also matches the `overlaps` message
of the next branch, because the test's regex is `/can never fire|overlaps/`. That is an old weakness of the case, not of the port; left as it was.

## Real validator, before and after

`node tools/validate.mjs --no-manifest` on `app/content`: output byte-identical before and after (diff empty). 0 errors, 5020 warnings.
Per tag, before and after the same: key-length 1477, O2-long-sentence 901, O2-explain-answer 566, negative-key 240, no-constraints 210, near-miss 190,
shown-arithmetic 163, float-artefact 110, wrong-band 87, percent-form 74, float-example 40, O2-no-slip 37, tight-band 26, O2-prose-prompt 8,
math-thousands-comma 7, accept-form 6, shuffle-false 2 (the rest are untagged).

## Owed or left

- No rule was changed in `validate.mjs`. Batching or in-process runs were not needed: 0.4 s a run keeps the largest file at 28 s.
- The mini root is hand-maintained (README inside). A change to the real `algo-think/l1-counting-work` or `equations/problems-3` does not flow
  into it; several cases plant into fixed screens of those copies.
- `docs/AUTHORING.md` is untouched: authors do not run these tests. Backlog and inbox files untouched for the main session to number.
