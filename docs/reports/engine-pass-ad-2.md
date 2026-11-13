# Engine pass AD part 2 (items 972 and 973)

Status lines for `docs/ENGINE-BACKLOG.md` (not edited, the numbering agent owns it):
- 972. Done: `fresh-check` same-course mode (`app/tools/same-course-reuse.mjs`, called by `fresh-check.mjs --file` for `problems-<n>.json`, `--same-course` for any course file, `--no-same-course` off), a `static` CI step, waiver file, tests, docs. (d), a renamed index or variable, not done: it needs a symbolic normal form of every displayed formula; the 893 formula and parameter advisories catch the unrenamed case.
- 973. Done: cause found and fixed. `--shard` partitioned by position, so new items moved others to a shard whose cache did not hold them.

## 972 same-course reuse

Each item and each part (with its stem) of a file is held against every other file of the course (lessons with quizzes, reviews, homework, other problem sets; `fluency-*` left out). All 106 sets plus the app-wide frequencies take about 10 s.

| kind | rule | level |
|---|---|---|
| matrix | `pmatrix`/`bmatrix`/`vmatrix`, `[[..]]` strings, canvas `rows`, `state.matrix`; equal up to a non-zero scalar and a transpose; identity, zero, vectors, fewer than three distinct sizes, symbolic ignored | error |
| text | longest shared word run after case, punctuation, numbers and maths become `#`; stock question and answer-format sentences, and any sentence in 5 or more files, cut out first | error from 12 words, warning from 10 |
| numbers | 3 or more distinctive numbers (stated, or keyed as a whole number or at most 3 significant figures), or 3 or more under one scale factor (whole 2 to 12, 1.5, 2.5, or reciprocal), values within 0.2% count once; not distinctive: whole numbers up to 20, years, round stock numbers, constants, a number in more than 15 files of other courses | warning |

Calibration on the 106 sets (waivers off):

| draft | numbers | matrix | text | read | false positives |
|---|---|---|---|---|---|
| first (every number, 8-word runs, no sentence filter) | 400 | 9 lines | 173 | 26 of 582 | about 23 of 26 (scale factors on bands and rounded values, format sentences, stock questions) |
| tuned (final) | 2 lines | 9 lines | 2 error | all 13 | 1 of 13 (a k-means procedure sentence, borderline) |

Tuning steps: scale factors only if simple and on clustered values; keyed numbers only if whole or at most 3 significant figures (computed tails are consequences); sentence-level boilerplate by frequency over files; stock question and format sentences dropped; matrices keep no frequency filter (a staple matrix was a true hit). Recall is measured only by the synthetic tests; the four review files' reuse findings no longer appear in the content (fixed there).

Pre-existing true hits (waived in `app/tools/same-course-waivers.json`, reason "pre-existing, owed a content fix"; content untouched):

| file | item | kind | source | evidence |
|---|---|---|---|---|
| eigen/problems-2 | p-oval-pond | matrix | homework-4 items[5], l6-bowls quiz[3], problems-4 items[2] | $\begin{pmatrix}1&2\\2&4\end{pmatrix}$ literally |
| eigen/problems-4 | p-track-laps | matrix | homework-4 items[5], l6-bowls quiz[3], problems-2 items[0] | the same matrix |
| vectors/problems-3 | p-goat-feed | matrix | l10 quiz[1], l9 screens[5], l5 screens[3] | $0.1 \times \begin{pmatrix}4&1\\2&3\end{pmatrix}$ and a third matrix scaled |
| analysis/problems-3 | p-cube-root-greedy | text | review-3 items[4] | 12 words "if the total is at most # take the next unused positive term" |
| stat-learning/problems-4 | p-order-sizes | text | l16 screens[0], homework-4 items[6] | 13 words of the k-means step (borderline: a stock procedure) |
| series/problems-2 | p-app-users | numbers (warning) | homework-1 items[4], l7 quiz[0] | 324, 972, 2916 shared; 972, 1456, 2912 are 4 times 243, 364, 728 |

Gate: the `static` job runs `node tools/same-course-reuse.mjs --all` after the validator (one step in `.github/workflows/acceptance.yml`). Validator: 0 errors; `manifest.json` restored, not committed. Tests: `test-fresh-check.mjs` has 14 new checks (doubled matrix, a third of a transpose, identity and zero ignored, number set times four, three shared numbers and two not, shifted sentence, small numbers and 3/8 and a year, a boilerplate sentence, `--no-same-course`, item waiver, the `--all` gate). Docs: `AUTHORING.md` (after exam freshness), `CI.md`.

## 973 the 18 minutes

Run 10 (id 43325249545), `extras problems-1 mobile`: `changed: 39 of 54 items`, 18.5 min; the cache restored from run 9 held 48 entries. The 12 new sets are 6 per shard. Locally, the item hashes of commits 383bf79 (run 9) and 4573024 (run 10) differ for only 5 of 94 existing sets (the five edited files), so the hash has no course-wide or manifest dependency (the course listing in the hash only touches the four courses that gained files). The cause is `--shard i/n` by list position: inserting sets shifts every later set to the other shard, and each shard's cache holds only its own items. The same shift hit the `play` legs for items after the insertion. Mobile and desktop keys were right; the cold-cache and `restore-keys` design was not at fault.

Fix: `playthrough.mjs` shard = sha1 of `kind|id` mod n. Cost: with 16 shards, shards hold 112 to 146 items (mean 128), longest leg about 14% longer in a full run. The first push after this replays everything once. `test-playthrough-changed.mjs` adds a check that two new sets move none of the other 107. Documented in the playthrough header, `AUTHORING.md` (long runs) and `CI.md`.

## Run

`test-fresh-check.mjs` (all passed), `test-playthrough-changed.mjs` (all passed), `ci-coverage.mjs` (0 problems), `validate.mjs` (0 errors), `playthrough.mjs --problems eigen/problems-2 --changed` (green) and `--all --changed --shard 1/16 --list`. Nothing committed (the session forbids git writes).
