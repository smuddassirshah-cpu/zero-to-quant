# Zero to Quant

An interactive learning app that takes one adult from school arithmetic to quant-interview readiness, and towards the research habits of a machine-learning lab, along the curriculum in `docs/curriculum.md`: Stages 0 to 3, 3,390 mapped hours on the trader track, 3,450 on the researcher and ML research tracks and 3,470 on the developer track. It teaches the way Brilliant does: short screens built around a diagram the learner manipulates, immediate diagnosed feedback, spaced review, homework and timed papers. Brainy Bertie, a small Einstein-style bobble head, is the mascot and the face of an AI tutor that never becomes the source of truth.

One TypeScript codebase builds two targets:

- a claude.ai Artifact for daily use on any device, whose tutor runs on the viewer's own Claude account and whose progress syncs through the Artifact's database;
- a static, offline-capable web app (local, or deployed behind access control until a content licence is chosen: `docs/PLAN.md` 12 decision 13) with full Python in the browser (Pyodide with NumPy, pandas, SciPy, statsmodels, scikit-learn and matplotlib) for code drills, whose tutor calls a small proxy that holds the API key.

## Status

The Blueprint carries the owner's decisions of 7 October 2026 and was approved by him that day. Build stage 1 (scaffold, toolchain and CI) produced the toolchain below and an empty app that boots on both targets; `STATE.md` tracks the build stage by stage.

## Getting started

Prerequisites, at the versions CI uses:

| Tool | Version | How |
|---|---|---|
| Node.js and npm | 22.22.0 and 10.9.4 (`.nvmrc`; at least 22.18, whose built-in type stripping runs the tools) | `nvm install` in the repository |
| Go | 1.24 or later | Builds the pinned gitleaks; Go fetches the toolchain the module asks for |
| Python | 3.12.15 (`tools/py/.python-version`) | System, `pyenv` or `uv python install`; only the CI packages need it. Another 3.12 patch works locally with `UV_PYTHON=/path/to/python3.12` |
| uv | 0.8.17 | `python3 -m pip install --require-hashes --only-binary :all: -r tools/py/uv-bootstrap.txt` |

From a clean clone:

```sh
npm ci                        # exact pins from package-lock.json; installs the git hooks
npm run setup:gitleaks        # gitleaks 8.30.1 into .zq/bin, verified by Go's checksum database
npm run check:py              # uv lock --check, then uv sync --locked (tools/py)
npm run check                 # types, lint, format, CSS, knip, VITE_* names, licences
npm run test:coverage         # unit tests with the coverage floors
npm run test:py               # zqverify, the Python twins, on CPython 3.12
npm run test:browser          # package tests in Chromium, Firefox and WebKit
npm run build                 # both targets, the Artifact page fragment, release budgets
npm run size                  # entry and stylesheet size limits
npx playwright install chromium
npm run test:e2e              # the empty app boots on the dev server, the web build and the Artifact host
npm run check:secrets         # gitleaks over every commit of every ref
```

Day to day: `npm run dev` serves the development page at `http://localhost:5173/`; `npm run serve:artifact` serves the built Artifact through the local host emulator at `http://127.0.0.1:4174/`.

The git hooks (pre-commit: format, lint, CSS and staged secrets; pre-push: full-history secrets, every static check, unit tests, `npm audit` and `pip-audit`) refuse to run without lefthook, gitleaks and uv installed. They are early warnings; CI is the gate that decides a merge (`docs/DECISIONS.md` B6).

## Repository settings the owner applies

These live in GitHub's settings, not in the repository, and only the owner can set them:

1. **Branch protection or rulesets** on `main` and on `stage/*`: require a pull request; require the status checks `static`, `unit`, `build` and `secrets` from `ci`; block force pushes and deletions. Two settings wait: `visual-approved` (from `label-guard`) becomes a required check only after stage 1 reaches `main`, because the guard has not run yet ([unverified] whether GitHub reads it from the base or the default branch); and code-owner review on `main` waits for a separate identity for the build sessions (`docs/DECISIONS.md` B5), because the sessions' pull requests are authored by the owner's account and GitHub refuses an author's approval of their own pull request [recalled], so requiring it now would block every merge into `main`. No branch is protected today [measured]. Branch protection on a private repository may need a paid plan [recalled, unverified]; if the settings page does not offer it, the rules stay procedural.
2. **Identity.** The build sessions' GitHub connection acts as the owner's own account [measured], so GitHub cannot stop a session merging into `main` or applying `visual-approved`; `CLAUDE.md` hard rule 3 forbids both (`docs/DECISIONS.md` B5).
3. **Actions.** Allow GitHub Actions for the repository; CI uses only GitHub's own actions (`actions/checkout`, `setup-node`, `setup-python`, `setup-go`), which a later session pins to commit SHAs.

## Where things are

| Path | What |
|---|---|
| `docs/PLAN.md` | The blueprint: every architectural decision, the threat model, and the build stages with their definitions of done |
| `docs/ARCHITECTURE.md`, `WIDGETS.md`, `CONTENT-FORMAT.md`, `AI-TUTOR.md`, `ASSESSMENT.md`, `BERTIE.md`, `CURRICULUM.md` | The appendices; `PLAN.md` section 1 lists what each owns |
| `docs/DECISIONS.md` | Decisions with their rejected alternatives, waivers, raw-HTML sink justifications, spike results |
| `CLAUDE.md` | The build protocol every build session follows |
| `STATE.md` | Stage status, gates, open questions and the next action |
| `docs/curriculum.md`, `docs/curriculum/` | The owner's curriculum and the fifteen item files that detail it |
| `docs/design-research.md` | The researched Brilliant recreation spec |
| `prototype/` | The approved Stage 1 clickable mockups (`prototype/README.md` says how to open them) |
| `spikes/` | Measured platform spikes |

## How the build is gated

- The build runs in the numbered stages of `docs/PLAN.md` section 11: the engine and its domain services, every P0 widget batch, Bertie and the tutor, progress and assessments, the two builds, then content depth-first from 0.1, one level per gate.
- Each stage has its own branch, `stage/<n>`. Every pull request is reviewed by a second agent session and merges into that branch; the owner reviews the stage as a whole, and the next stage starts only after his literal reply "approved, continue". Only the owner merges into `main`.
- Every auto-graded numeric, symbolic and set answer, and every item generator, is proved by two independent implementations in CI; code drills are graded by authored test suites that CI runs against a reference solution and known-wrong solutions; long-form work is marked against authored rubrics, and in a gate each rubric point counts the lower of the learner's and Bertie's marks.
- The Artifact publishes only files built from this repository's own sources: third-party JavaScript loads from CDNs at pinned versions, and every Python, SQL and C++ drill hands off to the web app.

## Licence

The code is MIT licensed (`LICENSE`): configuration, `packages/`, `src/`, `tools/`, `tests/`, `proxy/` and the generator code in `content/generators/`. The curriculum, lesson content and documentation (the rest of `content/`, `docs/`, `prototype/` and the prose files at the root) are not licensed for reuse until the owner chooses a content licence (`docs/PLAN.md` 12, decision 8). The repository is private and is not made public before that decision.
