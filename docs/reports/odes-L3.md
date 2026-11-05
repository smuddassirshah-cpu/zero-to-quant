# odes level 3: Systems and stability

Author: content agent (odes L1 to L3 wave). Brief: `docs/briefs/odes.md` `## Level 3`.

## Files

| file | screens / items | quiz | notes |
|---|---|---|---|
| `l10-first-order-systems.json` | 11 screens | 4 | hook: drag $\mathbf{v}$ and watch $\mathbf{A}\mathbf{v}$ (plane points and arrow segments, derive); companion matrices as `expression` matrix answers (2 by 2 and 3 by 3); two-factor model on `matrix` canvases; trap with the wrong-constants curve; defective case; `code` companion and eigen-solve |
| `l11-phase-plane.json` | 11 screens | 4 | saddle, node, spiral, centre and a line of equilibria as `field` + dragged `trajectory`; centre's conserved $4x^2 + y^2$ as an `order`; turning trap with $\mathbf{B} = \mathbf{A}^T$; `code` trajectory and turning |
| `l12-stability.json` | 10 screens | 4 | trace-determinant map with a dragged point and a derived caption naming the type; `table` widget for $\tau$, $\Delta$; `drag-point` for eigen l14's matrix; slider on $b$ moving l9's oscillator across the parabola; unit circle for the discrete test; `code` classify |
| `l13-linearising.json` | 10 screens | 4 | predator and prey `field` with a hidden linearised `field` and a second trajectory; crowding slider `c` in the field formula; conserved $H$ as an `order`; zero-eigenvalue edge case; `code` jacobian with `classify` in a hidden `prelude` |
| `review-3.json` | 9 items | | difficulty 2 to 4, every lesson, one recall of l9's damping as a system (`r-damping-system`) |
| `homework-3.json` | 8 items | | difficulty 3 to 5; `h-equilibria` is the performance task (`code`, difficulty 5, Newton with the numerical Jacobian; `jacobian` and `classify` in the prelude); `h-regions` order derivation of the map; `h-spreads` longform with a 10-point rubric |

Performance task: the level is rule-matched (l10's objective starts "Write"), so `h-equilibria` carries `"performance": "code"` (5 hidden tests, 1 example).

Phase portraits: every portrait is a `plane` `field` (normalised, `colourBy: "magnitude"`, `equal: true` for linear systems) with one `trajectory` from a dragged start (`back: true`): 8 screens in l11, 1 in l12, 8 in l13 (l13 screen 5 adds a second, hidden field for the linearisation and a second trajectory). Closed-form curves are kept for l10, where fitting the constants is the point (4 screens), and for eigenvector lines (4 screens of l11).

Classification choice (stated in l12 screen 9 and its `how`): on the parabola $\tau^2 = 4\Delta$ `classify` returns the node of that side, so $b = 4$ is `"stable node"`; $\Delta = 0$ returns `"degenerate"`.

## Self-check (SESSION PROTOCOL 4)

1. `node tools/validate.mjs`: 0 errors; no warnings on any level 3 file.
2. Voice scan over `app/content/courses/odes/`: 0 explanations over three sentences, 0 sentences over 20 words.
3. `python3 docs/reports/odes-L3-numbers.py`: 0 failures, exit 0. Route 2 is `np.linalg.eigvals`, a scaling-and-squaring Taylor matrix exponential, or a fine-step RK4 solve of the nonlinear system (periods from crossing times).
4. Playthrough with `--local-cdn`: l10 to l13, review-3 and homework-3 green with `--mobile` and without. Homework: "1 performance starter fail".

`node app/tools/closure.mjs --target pdes/L2` now reaches no unwritten `odes` level; the only unwritten course it reaches is `complex` (level 1).

## Numbers (source: the script; both routes agree)

Eigenpairs: $-1, -2$ on $(1, -1), (1, -2)$; $-2, -0.5$ on $(1, 0), (4, 3)$; 3 and $-1$ on $(1, 1), (1, -1)$; 2 and $-4$ for the trap. $c_1 = \tfrac1{150}$, $c_2 = \tfrac1{300}$, $\mathbf{x}(1) = (0.008989, 0.006065)$, 1.3863, 0.3466, 0.3679, 0.208833 and 4.670774 (code tests), $(2.5441, 1.9376)$, $(-1, -2)$, $e^{-\pi} = 0.0432$, $\ln 2 = 0.6931$, $\ln 2/3 = 0.2310$. $\tau$, $\Delta$: two-factor $(-2.5, 1)$ with $\tau^2 - 4\Delta = 2.25$, spiral $(-2, 5)$, saddle $(2, -3)$, centre $(0, 4)$, companion $(-3, 2)$, eigen l14 $(-4, 3)$, trap $(-2, -8)$, $b = 4$ at $(-4, 4)$, drift $(-0.5, -0.14)$ with eigenvalue 0.2. Predator and prey: $(3, 2)$, $\Delta = 0.75$, $\pm 0.8660i$, 7.2552, 7.42 through $(5, 2)$, $H$ conserved, crowded $(3, 1)$ with $-0.25 \pm 0.5590i$ and $\Delta = 0.375$, cycle 7.26. Review: $c_1 = 2$, $\Delta = -1$, 0.433, 0.25, 0.3466. Homework: 9.7294, 14.7781 (distractor), $-1 \pm 2i$, $\Delta = -1$, $\sqrt5/4$, 0.3466 and 0.1733.

## Proposed course.json change

None.

## Backlog

Two bullets in `docs/BACKLOG-INBOX.md` under "Raised later (odes level 3)".
