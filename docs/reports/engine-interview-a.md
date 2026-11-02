# Engine pass A: timed mock assessments (items 450 to 454)

Source: `docs/briefs/interview-plan.md` section f, bullets E1, E2, E4, E5 and E6. Numbered 450 to 454 in `docs/ENGINE-BACKLOG.md` (449 was the highest), marked done there; item 129 is marked covered by 454. The five bullets are removed from `docs/BACKLOG-INBOX.md`; E3, E7 and the rest of the interview bullets stay.

## What changed

| Item | Bullet | Where |
|---|---|---|
| 450 | E1 scoring, `passNet`, net score on results | `js/screens/exam.js`, `js/engine/mock.js` (`tally`, `need`, `passed`), `js/state.js` (`examFinished` takes `extra`) |
| 451 | E2 `navigation: "forward"`, `skip: false` | `js/screens/exam.js`, `css/screens/exam.css` (`.is-fwd`) |
| 452 | E4 generated items | new `js/engine/arith.js` (`ZQ.arith`), shared with Today's warm-up (`today.js` `makeProblem` now calls it) |
| 453 | E5 mock exam kind | `exam.js`, `ZQ.content.mocks()` (`content.js`), Review "Mock assessments" card (`review.js`), You history (`you.js`), `validate.mjs` |
| 454 | E6 `timed` sets | `review.js` (`setPage`), `player.js` (`runSet().finish()`), `validate.mjs` |

New files: `app/js/engine/arith.js`, `app/js/engine/mock.js` (both in `index.html`), `app/content/exams/mock-sample.json` (the only content file touched). Docs: `docs/AUTHORING.md` section 5 (Mock assessment, Paper fields, Generated items, Timed sets) and a rules paragraph in section 7; `app/README.md` file table.

## Behaviour worth knowing

- Marks: a paper's net is `right*R + wrong*W + blank*B`, "blank" meaning no answer given. `pass` is now a share of the maximum marks (identical to the old rule under default scoring, so `topic-*` and `stage-*` are unchanged); `passNet` is absolute. Both together is a validator error.
- Forward papers: no navigator, Mark or Back; jumping ahead is refused; each answer locks as the learner moves on; Enter moves on; with `skip: false` Next waits for an answer, otherwise it reads Skip on an unanswered question.
- Generator: `{ generator: "arith", mix, n, options }` expands at the start of the attempt. Near misses are the reverse operation, a misplaced decimal point and a slipped digit; options are shuffled by the seeded stream. Seed is per attempt, or `#exam/<id>/<seed>`, stored on the attempt as `seed`. Generated items carry no id, so they never join the redo queue. Ranges in `mix` go on `add` or `mul` and apply to the reverse operations.
- Mocks: `parts` (papers and checks) or one paper's fields at the top level; `style` sets the track colour; no XP; attempts keep `net`, `max`, `wrong`, `blank`, `seconds`, `seed`. Result page adds a "Score trend" card and swaps the XP badge for the attempt number; "By skill" is hidden when no item names a skill. Review lists mocks above Exams. You shows net scores and net pass marks.
- Short papers: the amber low-time state starts at a quarter of the clock when that is under five minutes (unchanged for papers of 20 minutes or more).
- Timed sets: `timed: { seconds, lockAtZero }` at the top of a level review file, or `#practice/timed/<seconds>`. Countdown and live score in the header; at zero a locking set checks a ready answer, then ends, the rest counts as missed (joins the redo queue); the summary says so. Without `lockAtZero` the clock is a guide. Not built: a timed homework, a timer on lessons, and a deck (E7 does not exist yet; a deck passes the same field to `setPage`).
- E6 coverage caveat: an exam file cannot carry `timed`, so the sample mock cannot exercise it. The playthrough tests it on any review whose file has `timed` with `lockAtZero`; no such review exists in the content yet, so it was verified on a scratch copy of `app/` (see below). Until a content review uses it, `--all` does not cover E6.
- A bug found on the way and fixed: on phones the stage-exam "Part by part" rows inherited the result-card grid areas and squeezed their text; fixed in `exam.css`.

## Tools

- `validate.mjs`: `mock-<id>` exam ids; mock rules; paper rules (`scoring`, `pass`/`passNet`, `navigation`, `skip`) for topic, stage and mock; generator entries (not in topic exams); `timed` on reviews (an error on homework). Scratch cases (a copy of `app/` with bad mocks and a bad `timed`) each gave the expected error lines; a valid mock with a top-level paper, a `mix` range and a fractional-free scoring gave none.
- `playthrough.mjs`: plays `mock-*` like `--exam` (included in `--exams` and `--all`); on a forward paper probes jump ahead, going back and, with `skip: false`, moving on unanswered; generated items repeat for the same seed and differ for another; a second sitting with `ZQExam.setRemaining(0)` must submit itself, say "Time ran out", be kept as an extra attempt and carry a net; a timed locking review gets the same clock test (`ZQSet.setRemaining(0)`). No real timer is ever waited for. Also: a hash change is forced before replaying the same route, which previously hung a repeat visit.

## Verification (from `app/`, local CDN `scratchpad/pkgs`)

- `node tools/validate.mjs`: 0 errors.
- `--exam mock-sample`: passes (11 items, net 14 of 14, mock checks ok). `--exam topic-1.5` and `--exam stage-0`: pass. `--routes-only`: passes. The Today warm-up still starts and runs (checked by hand).
- `--set number-sense/review-1` with `timed` added in a scratch copy: clock test and full play pass.
- Screens checked at 390 px and 1280 px in light and dark: mock start card, forward paper (including 390 px with the amber timer), between-papers page, free paper with navigator sheet, checks page, result with trend (first and second attempt), Review hub with the mock card, You history, timed review start card, running header and time-out summary.
- Full `--all` run: see the end of this file.

## Left for later

- Auto-advance on pick for forward choice papers (80 questions need a pick and a Next or Enter each).
- E3 (banks), E7 (decks) will want `timed` passed through; `setPage` already accepts it.
