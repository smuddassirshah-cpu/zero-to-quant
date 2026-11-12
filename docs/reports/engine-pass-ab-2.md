# Engine pass AB-2: bank part 2 (B2-E1 to B2-E6 and the bank inbox bullets)

Items 920 to 930 of `docs/ENGINE-BACKLOG.md` (status lines there). No file in `app/content/` was edited; no git write command was run.

## Status

| Item | Requirement | Status |
| --- | --- | --- |
| 920 | B2-E1 Python `code` items in the bank | done |
| 921 | B2-E2 `--routes-only` pace check reads the second item's `pace` plus 20 s | done |
| 922 | B2-E3 `--bank --mobile` really runs at 440 x 956 | done |
| 923 | B2-E4 `Bank("<file id>")` in `numbers_lib.py` | done |
| 924 | B2-E5 `[bank-family]` warning | done |
| 925 | B2-E6 results row shows `widget.prompt` for a `longform` item | done |
| 926 | inbox: `answerWrong(id)` and `--bank --why` | done |
| 927 | inbox: fresh-check reads shuffled options one at a time | done |
| 928 | inbox: `[wrong-band]` on a rounding half | open (not a bank tool; needs a rule decision) |
| 929 | inbox: fresh-check advisory for a shared 8-word run at any share | done (reads the stem, `prose` and `question`) |
| 930 | inbox: fresh-check sees set-ups, not wording | open (needs a parameter extractor) |

## What changed

- `app/tools/validate.mjs`: `checkBank`/`checkParts` refuse only a C++ code item or part; `language` may be absent in the bank; `bankCodeRules` (`[bank-code]`: error for no `solution` or a starter equal to it; warnings for a pace outside 240 to 480, a test count outside six to ten, and a `how` "runs N hidden tests" whose N is not the test count); `[bank-family]` (`bankFamilies`: skill ids of every `course.json`, first tags of course items, and the engine family `mental-arithmetic`; sample files skipped).
- `app/js/engine/player.js` (runSet test hook): `probe()` grades the open item or part without marking it; `answerWrong(id)` (a `unit: "%"` field is typed as `6.18%`; no id keeps the old behaviour).
- `app/js/screens/review.js`: `stemOf` shows `widget.prompt` for a longform item. The deck page itself already ran code items (it is `setPage`, as a level review is); nothing else was needed there. `drill-worker.js` was not touched, so the recursion behaviour (917, 919) is as it was.
- `app/tools/playthrough.mjs`: `bankPlay` rewritten (code starter check then solution; viewport loop over `[DESKTOP, ...EXTRA]` with a sideways-scroll check after the answer, after the check and on the result page; `--why`; longform row check); `bankChecks` second-item pace.
- `app/tools/fresh-check.mjs`: drill code names against a bank item; shuffled options broken apart; stem-run advisory (`--question-run`, `--no-question-run`).
- `app/tools/numbers_lib.py`: `Bank` class; `_walk` reads `[<item id>]`.
- Tests and fixtures: `app/tools/fixtures/bank-code/fixture-code.json` (two code items, one good, one whose starter already passes), `app/tools/test-bank-code.mjs` (validator cases incl. `[bank-family]`, playthrough desktop and `--mobile`, `--why`), a `Bank` case in `test-numbers-lib.py`, new cases in `test-fresh-check.mjs`.
- Docs: `docs/AUTHORING.md` section 5 (bank bullet incl. the new "A `code` item" bullet, Drawn items "Code", validator rules, exam freshness, Recompute script); `docs/ENGINE-BACKLOG.md` 920 to 930.

## The `code` item shape authors write

```json
{ "id": "integer-division-lot-round", "difficulty": 3, "skills": ["..."], "tags": ["<family>"], "role": ["developer"], "style": "coding", "source": "Original", "pace": 300,
  "prose": "signature and one worked call", "question": "Complete `lot_round`.",
  "widget": { "kind": "code", "language": "python", "starter": "def lot_round(qty, lot):\n    ...\n",
    "examples": [ { "call": "...", "expect": "...", "compare": "equal" } ], "tests": [ 6 to 10 cases ],
    "how": "Submit runs N hidden tests. Each result must equal the expected whole number.", "solution": "..." },
  "feedback": { "correct": "...", "generic": "..." }, "explain": { "text": "..." } }
```

`language` may be left out. `how` wording (the s1 proposal): `equal` integer result "must equal the expected whole number.", `compare: "fraction"` "must equal the expected fraction exactly.", otherwise "must equal the expected value."; N is the real test count. Pace 240 to 480. The starter must fail the tests and the solution must pass every one (the playthrough checks both). Python only; a C++ code item is an error.

## B2-E3: the 32 live bank files at 440 x 956

`node tools/playthrough.mjs --mobile --bank <8 files> --local-cdn <pkgs>` in four batches covering all 32 files (every file except `sample-draw`), each run at 1280 and then 440 px: 124, 200, 148 and 232 item plays, **0 failures**. No live bank file fails at 440 px. (The check is the same `scrollWidth > innerWidth + 1` test the other `--mobile` runs use, applied after the answer, after the check and on the result list.)

## Results

- `node tools/validate.mjs`: 0 errors, 4857 warnings. `[bank-family]`: 0 on current content (a first draft flagged 15 items, eight of the engine family `mental-arithmetic` and seven in `sample-draw`; both now handled). The other new warning class, `[bank-code]`, is 0 (no live code item).
- `playthrough.mjs --bank` on every bank file with `--mobile` (desktop and 440 in one run): all 32 files green (above). `--bank <file> --why` on 26 of the 32 files (all but `behavioural-2` to `-4` and `-6` to `-8`, which hold longform items only and have no slips; `behavioural-1` and `-5` were included): all green, so every `wrong[]` id and distractor of the live bank shows its own line. The first `--why` run on `finance-1` found my own bug (a `unit: "%"` field stores a fraction and is typed times 100); fixed, then green.
- `playthrough.mjs --routes-only` desktop and `--mobile`: All passed.
- Every `app/tools/test-*` file (45): all pass, exit 0. Long ones: `test-validate-problems` 531 s, `test-validate-fluency` 536 s (run in parallel with other loads), `test-validate-answer-forms` 281 s. None failed or timed out on its own. `test-bank-code.mjs` takes about eight minutes (each validator case copies `app/` and validates).
- Nothing in `app/content/` changed (`git status` shows only engine, tools, docs).

## Notes for the main session

- `ZQ.test.probe()` exists for the starter check; a code item that lies in a deck needs Python. In `--routes-only` a code item in the sitting is not held against the deck when Python cannot load (a note is printed), so a sandbox without `--local-cdn` still passes.
- The weekly mixed review already leaves out `code` items (`practiceKind`), so code items are only dealt by the deck and by a draw naming their file.
- 929 reads `prose` and `question`: the `finance-2` `fi-forwards-rich-forward` case from the inbox shares nothing of 8 words on current content, so it does not appear; the tool lists nine other advisories on `finance-2` (stock phrases such as "the interest rate is zero and"), which is the expected noise of an advisory at any share.
- Open: 928 (validator, rounding halves) and 930 (set-up reuse by named parameter).
