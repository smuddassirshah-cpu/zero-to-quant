# Fixtures of `test-fresh-check-retold-af.mjs`

The pre-fix text of the same-course reuse findings of the session AF reviews (`docs/reviews/review-problems-ensembles-1-3.md`, `-fin-ml-1-3`, `-validation-1-3`, `review-delta-ae-2.md`, `-ae-3`, `-ae-4`).

- `sets/<name>.json`: one problem set as the reader saw it, from git history (`git show <revision>:app/content/courses/<course>/<set>.json`), with `course` and `as` (the file name it takes in the temporary course) added to the top level.
  `ensembles-p2-first` 2a9b4c02, `ensembles-p2-ae2` c7ff2276^, `ensembles-p3-ae2` c7ff2276^, `ensembles-p2-ae4` and `-p3-ae4` HEAD of engine pass AF part 1, `finml-p1-first` 58aa5cd8, `finml-p3-first` fd75e12b, `finml-p3-ae2` 0db501e0^,
  `validation-p1-first` f78b7030, `validation-p2-first` 54354923, `validation-p3-first` 0d08a62f, `validation-p2-ae3` and `-p3-ae3` 151bfbfc^, `validation-p3-ae4` HEAD.
- `src/<course>/<file>.json`: the lessons, reviews and homework of the course that the sets are held against (HEAD of engine pass AF part 1, unchanged since the reads), with `canvas`, `starter`, `solution`, `tests`, `examples`, `data`, `rubric`, `skills`, `tags` and `model` left out (they are not read by the detector).

The test copies a set and its course's sources into a temporary `courses/<course>/` and scans it; word frequencies come from `tools/retold-model.json`, a snapshot learned over the whole content, so the result does not move with the content.
