# vector-calc level 1: Fields and line integrals

Author report (content wave 3, session T). Brief: `docs/briefs/vector-calc.md`, `## Level 1`.

## Files

| file | screens / items | quiz | notes |
|---|---|---|---|
| `l1-vector-fields.json` | 12 screens | 4 | drag-point hook, `place` with a `frames` control (four fields), gradient field over contours, trap (along vs across), edge (field undefined at the origin), portfolio-variance transfer (table, then a drag on the budget line) |
| `l2-line-integrals.json` | 11 screens | 4 | chord polyline with a `stops` control on `n` (one parametric entry using `floor`), speed arrow riding the arc, helix on `space`, trap (no speed), traced twice, code `scalar_line_integral`, Brownian total-move transfer |
| `l3-work-done.json` | 12 screens | 4 | `tap-regions` on plane segments, table of three works, `vectors` projection, rotation and radial fields round the circle, helix work on `space`, trap (clockwise; Show why patch reverses the path arrows), flow-line edge case, code `work`, P&L transfer |
| `l4-conservative-fields.json` | 12 screens | 4 | three paths give 4, `order` proof of the fundamental theorem with two distractor lines, the Clairaut test, `manipulate` to a potential, `expression` potential, `multi` equivalences, `space` potential $xyz$, vortex trap, loop that misses the hole, currency loop and gradient-holdings transfers |
| `review-1.json` | 9 items, `pass` 0.8 | | difficulty 2 to 4, every lesson |
| `homework-1.json` | 9 items | | difficulty 3 to 5 (two at 5); parts item (18.02-style two-path work), `expression` potential in space, `order` proof (gradient gives zero loops), two `code` items (`potential_at` + `passes_local_test` at 5, `work_polyline`), `longform` vortex (10-point rubric, full model), wire mass, planted test, currency loop |

## Gates

- Validator (`node tools/validate.mjs`): 0 errors; no warning names a level 1 file.
- Voice scan (`VOICE_BASE=app/content/courses/vector-calc/`): 0 explanations over three sentences, 0 sentences over 20 words.
- Numbers: `docs/reports/vector-calc-L1-numbers.py` exits 0, 227 of 227 checks, `lv.check_wrongs()` called. Every value is computed twice: a closed form and SciPy `quad` along the parametrised path (`both()` asserts they agree), then found at its JSON path. The "check by hand" lines are byKey texts that explain a slip without restating the wrong value; each was read.
- Playthrough with `--local-cdn`: all four lessons, review-1 and homework-1 pass at desktop and with `--mobile`.
- SciPy load time: about 7 s in the playthrough (the first code lesson took 24 s against 17 to 19 s for lessons of the same length without SciPy). Stated in the `how` of every SciPy code screen and item.

## Numbers (source: the script; key values)

Chords $4n\sin\frac{\pi}{4n}$: 2.828, 3.061, 3.121, 3.137. Segment $\int x\,ds = 7.5$ (no speed 1.5); arc $\int (x+y)\,ds = 8$ (no speed 4), $\int xy\,ds = 4$; helix length $2\sqrt2\pi = 8.886$, $\int z\,ds = 2\sqrt2\pi^2 = 27.915$; mean of $y^2$ on the unit circle $\frac12$. Seeded walk (numpy `default_rng(11)`, 64 normal steps of variance $\frac1{64}$, sub-sampled every 16 and 4): totals 1.760, 2.436, 5.696; expected $\sqrt n\sqrt{2/\pi}$ = 1.596, 3.192, 6.383, 12.766 at $n = 256$. Work: hook paths 1, 0, $\frac12$ (scalar slip 0.7071); $(y, x)$ on the parabola 1; rotation $\pm 2\pi$; radial 0; $\int y\,dx + x^2\,dy = \frac73$; helix $-\pi$; flow line $8\pi$; P&L £50 and £0. Level 4: 4, 4, 4; $f = x^2y + 3x + 2y^2$, work 13; $xyz$, work 6; vortex $2\pi$ round the origin, 0 round the circle at $(3, 0)$; FX loop 1.0005 (log 0.0005); $V$ P&L £15.50. Variance gradient $(0.046, 0.016)$, minimum $w_1 = \frac2{19} \approx 0.105$. Review: 40, $-18\pi$, 3, $2\pi$, $16\pi$. Homework: $\frac{13}{15}$, $\frac56$, 4, 36.801, 1.00584, £5,840.

## Departures from the brief (recorded, not errors in the brief unless stated)

- The 12-screen cap forced four l4 tasks into its quiz: "which result justifies line 2" (q1), the work 13 (q2), the space work 6 (q3) and the meaning of the non-zero currency loop (q4). The lesson keeps the order proof, the manipulate, the potential `expression` and the space potential `expression`.
- l2: the trap screen uses the arc (8 against no-speed 4); the segment's 1.5 slip is a `wrong` entry on the ladder and is named in the trap's byKey line.
- l2 and l3 helix screens are `problem`, not `ladder`, because they change canvas kind (plane to space).
- l3 code starter is a bare `pass`: a `return 0.0` stub would pass the radial and corner-B tests, which expect 0.
- Notation: the bold capital $\mathbf F$ is a field here, not a matrix (said once, in l1 screen 2). This is an exception to AUTHORING section 6.
- Brief: none wrong. "8 chords give 3.137" is $3.1365$ to 3 places.

## Proposed course.json change

None.

## Backlog

Two bullets in `docs/BACKLOG-INBOX.md` under "Raised later (vector-calc level 1)".
