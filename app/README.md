# Zero to Quant: the app

A single-user, Brilliant-style interactive teaching app for the curriculum in `docs/curriculum.md`. It runs from this static folder in Chrome. There are no accounts, no server code and no build step: plain `<script>` files, JSON content and `localStorage`.

## Run it

You need Python 3 (for `run.sh`) and Chrome or Chromium. Node is needed only for the checking tools below and for `tools/fetch-vendor.sh`, never to run the app. From a clone of `https://github.com/smuddassirshah-cpu/zero-to-quant.git`:

```sh
app/run.sh            # python3 -m http.server on port 8080 (pass another port as the first argument)
```

Then open `http://localhost:8080`. A fresh browser starts on `#setup` (name and initial, track, weekly hours and starting stage) and then opens `#today`. The app must be served over `http`, not opened as a file: content is fetched, and the Python and C++ workers are module workers that a `file://` page cannot start.

`run.sh` listens on all network interfaces, not only localhost. A tablet on the same network can open it at your computer's address; so can anyone else on that network.

To check that Python and C++ work, open `http://localhost:8080/#lesson/first-python/l1-calculator` and run its code check, then `#lesson/cpp/l1-source-to-program`. The C++ course is locked until its prerequisites are met: turn off Strict prerequisites under You, Settings, Study plan, then open the locked card and choose "Open anyway".

The grid tab on the left edge lists every screen and switches theme, motion and sound.

## What loads from the CDN

Only KaTeX is in the repository (`vendor/katex/`). Everything else loads from `cdn.jsdelivr.net` the first time a lesson needs it, and the browser caches it after that. The page also asks Google Fonts for its typefaces. Each library has an optional self-hosted fallback in `vendor/`, tried only when the CDN fails (see Self-hosting). With `vendor/` empty, the browser console shows 404 errors for those probes when the CDN fails. They are expected.

| Library | Version | Loaded by | When | Size |
|---|---|---|---|---|
| Pyodide (Python, with NumPy, pandas, SciPy, scikit-learn, statsmodels, matplotlib) | 0.27.7 | `js/screens/drill-worker.js` (`CDN`; `code.js` and `drill.js` pass `vendor/pyodide/` as the fallback) | First Python code widget or drill | The core is several MB; each package wheel downloads on the first import that needs it (a load is given up after 30 seconds with no data arriving, or at 5 minutes in all) |
| MathLive | 0.105.0 | `js/engine/grade.js` (`LIBS`) | First expression answer | 0.8 MB on disk for `mathlive.min.js` (the file the page loads; the package with fonts and sounds is 5.4 MB) |
| Compute Engine | 0.30.2 | `js/engine/grade.js` (`LIBS`) | First expression answer | 0.6 MB on disk for `compute-engine.min.umd.js` (the file the page loads; the package is 4.4 MB) |
| YoWASP clang | 21.1.4-3 | `js/engine/widgets/cpp-grade.js` (`CLANG`) | First C++ code widget | About 26 MB gzip (see the table below); given up after 90 seconds with no data arriving, or at 5 minutes in all |

MathLive and Compute Engine share a budget: 6 seconds for each CDN script, then up to 4 more for its local copy in `vendor/` (10 seconds in all). If either has not loaded by then, the expression widget still works, with less help:

- No MathLive: a plain text box replaces the maths field, with the note "Type the expression as text: use / for fractions, ^ for powers and * for products."
- No Compute Engine: answers are matched as normalised text against the lesson's `answer` and `accept` list, not checked algebraically.
- No Pyodide: a CDN that refuses the request (a network error, a 403 from a proxy) is passed over at once, and one that holds the connection open without answering after 8 seconds. With no copy in `vendor/pyodide/` the page then reports the failure within about 8 seconds at most. While bytes are arriving the load carries on, so a slow first download still succeeds; it is given up after 30 seconds with nothing arriving, or at 5 minutes in all. The code widget then shows "Python is not available here". Check does not call that a wrong answer: the lesson player shows a neutral "Python could not load" with no XP, no attempt, no Redo entry and a Try again that retries the load, and the drill page shows the same with its own Try again. A package wheel that cannot be downloaded (NumPy, pandas) is reported the same way and stops the run; the same stall rule applies to it. Until it loads the check says "Python is still loading."
- No clang: the same, with "C++ is not available here" and "C++ could not load" (the stall limit is 90 seconds, since the compiler also spends time building before it reports).

## Self-hosting (offline use)

`vendor/` is read only when the CDN is unreachable; with the CDN working nothing changes. Today the repository holds `katex/` only. One script fills the rest, in exactly the layout the code reads:

```sh
app/tools/fetch-vendor.sh            # into app/vendor (or give another folder as the last argument)
app/tools/fetch-vendor.sh --core     # Pyodide core only: --core comes first, then the optional folder
app/tools/fetch-vendor.sh --core /path/to/vendor
```

The script needs bash, curl, openssl, tar, bzip2, GNU base64 and Node.

| Folder | Read by | Holds |
|---|---|---|
| `vendor/pyodide/` | `drill-worker.js`; `code.js` and `drill.js` pass its absolute address as `indexURL` | The Pyodide 0.27.7 release: `pyodide.mjs`, the wasm, `pyodide-lock.json` and every package wheel. The worker tries the CDN first and this folder only when the CDN is unreachable and the folder has `pyodide.mjs`. |
| `vendor/mathlive/` | `grade.js` (`LOCAL`) | `mathlive.min.js` with `fonts/`, `sounds/` and `mathlive-fonts.css` beside it. MathLive finds `./fonts` and `./sounds` relative to its own script. It asks for fonts only when the KaTeX families are not already in the page, and the app has them from `vendor/katex/`, so in practice only `sounds/` is read (on a key press). |
| `vendor/compute-engine/` | `grade.js` (`LOCAL`) | `compute-engine.min.umd.js` |
| `vendor/yowasp-clang/` | `cpp-worker.js` | The package's `gen/` folder, directly in it (see the C++ section) |

The script uses the same sources as `tools/fetch-local-cdn.sh` (the Pyodide release tarball from `github.com`, the npm tarballs from `registry.npmjs.org`) and checks what it downloads: npm tarballs against the registry's sha512 integrity, and every Pyodide file against the sha256 in `pyodide-lock.json`. It skips folders that are already complete. The four folders are git-ignored; KaTeX stays tracked. The full Pyodide release is 389 MB to download and 762 MB on disk (351 packages). `--core` takes only the npm `pyodide` package (about 14 MB, no wheels): offline Python then runs the standard library only, with no NumPy, and a lesson that imports NumPy, pandas, SciPy, scikit-learn, statsmodels or matplotlib fails with an import error.

`node tools/test-vendor-fallback.mjs --vendor <dir>` checks all of it with `cdn.jsdelivr.net` blocked: a Python lesson, a C++ lesson, a NumPy lesson (its wheels load from `vendor/pyodide/`) and an expression lesson play to the end, MathLive registers its field and the Compute Engine grades an identity. `--absent` checks the opposite: without the folders Python and C++ report that there is no local copy, within 20 seconds even when the CDN holds the connection open, under the neutral headings "Python could not load" and "C++ could not load" (never "Not quite right.", no XP, Try again offered), and the maths editor falls back to a text box. CI runs both in the `python` leg of `tests-browser`.

`tools/fetch-local-cdn.sh <dir>` is a different tool, for `node tools/playthrough.mjs --local-cdn <dir>`, which intercepts jsDelivr in the test browser. It builds another layout (`<dir>/pyodide-0.27.7/package/`, `<dir>/mathlive-0.105.0/package/` and so on, about 870 MB) and does not populate `app/vendor/`.

## Check the content

```sh
node app/tools/validate.mjs             # schema and teaching rules; exit code 1 on any error
node app/tools/validate.mjs --summary   # plus lesson counts per course and every mapped lesson not yet written
```

The validator implements `docs/AUTHORING.md` section 7. Missing lesson, review and homework files are warnings: the course map shows them as "Not yet written". When there are no errors it rewrites `content/manifest.json`, the list of authored files the app reads so it never requests a file that is not there. Run it after adding or renaming any content file.

## Folders

| Path | What it holds |
|---|---|
| `index.html` | The page: every stylesheet and script, in load order |
| `run.sh` | Local static server |
| `css/` | `tokens.css` (colour, type, motion), `components.css`, `widgets.css`, `canvases.css`, one file per screen in `screens/` |
| `js/core.js` | Router (`#screen/param/param`), icons, KaTeX helpers, sound, motion, sheets, the shell header |
| `js/state.js` | `ZQ.state`: the learner's state in `localStorage['zq.state']`, typed mutators, XP, MP, mastery, redo queue, streak, hours, export and import |
| `js/content.js` | `ZQ.content`: loads `content/curriculum.json` and every `course.json`, then lessons, reviews, homework, exams and drills on demand |
| `js/art.js` | Code-drawn course art (`ZQArt(kind)`) |
| `js/engine/` | Lesson player, grading helpers, seeded simulation, one file per widget and per canvas |
| `js/screens/` | One file per screen: setup, today, learn, course, lesson, review, exam, drill, you, system, plus the drill's Python worker and the C++ compiler worker (`cpp-worker.js`) |
| `content/curriculum.json` | Stages, topics with hours, tracks and resources, and the course list |
| `content/courses/<course>/` | `course.json` (skills, levels, lesson names and objectives), then `<lesson>.json`, `review-<n>.json`, `homework-<n>.json` as they are written |
| `content/exams/` | `topic-<topic>.json`, `stage-<n>.json` and `mock-<id>.json` (timed mock assessments) |
| `content/drills/` | `index.json` and one file per code drill |
| `content/warmup.json` | Settings for the two-minute mental arithmetic warm-up; its operations also feed generated exam items (`js/engine/arith.js`) |
| `content/courses/<course>/fluency-<lesson>.json` | A generated fluency set (20 fresh typed-answer questions, JSON only; `docs/AUTHORING.md` section 16). Engine: `js/engine/gen.js` (the safe evaluator, formats and drawing), `js/screens/fluency.js` (route `#fluency/<course>/<set>`) |
| `content/courses/<course>/problems-<n>.json` | A level's problem set (3 to 5 chained problems, each with 3 to 5 graded parts; untimed, repeatable, never a gate; `docs/AUTHORING.md` section 5). Route `#problems/<course>/problems-<n>` in `js/screens/review.js` (the shared set page), saved in `ZQ.state.problems`, listed on the level review's card on the course map |
| `js/screens/weekly.js`, `tools/test-cumulative.mjs` | The weekly mixed review (route `#weekly`, due on Today once a week; selection in `js/engine/select.js`, `ZQ.select.weeklyReview`) and its tests |
| `content/manifest.json` | Generated by the validator |
| `tools/validate.mjs` | Content validator (node, no dependencies) |
| `tools/fluency-sample.mjs`, `tools/test-fluency.mjs`, `tools/fluency-rules.mjs` | Draw items from a fluency set; grade every family in the real browser; the rules the validator applies. Fixtures in `tools/fixtures/fluency/` |
| `tools/test-fluency-reach.mjs`, `tools/audit-plain-functions.mjs` | Unit tests of the authoring reach of Fluency families (functions and `pi` and `if` in `let`, `wrong[].when`, the `cfrac`, `(frac)`, `sfN`, `mono` and `falling` formats; ENGINE-BACKLOG 838 to 840); the audit of plain-text function names in graded answers (836) |
| `tools/test-validate-problems.mjs`, `tools/test-problems.mjs`, `tools/fixtures/problems/` | Scratch cases for the problem-set validator rules; the runtime test (save, XP, hours, weekly review pool, the real player); the fixture set (never content). `node tools/playthrough.mjs --problems <course>/problems-<n>` plays one |
| `tools/drill-constraints.mjs`, `tools/test-drill-constraints.mjs`, `tools/test-drill-page.mjs`, `tools/fixtures/drill-page/` | Machine-readable drill `constraints` (reader shared with the validator; `[no-constraints]`; ENGINE-BACKLOG 866) and the drill page limits (shared comparison, `setup`, `raises`, lists, long spans, `allocCheck`; 861 to 865): unit cases plus a played fixture drill, desktop and `--mobile` |
| `vendor/katex/` | KaTeX, vendored (`vendor/pyodide/`, `mathlive/`, `compute-engine/` and `yowasp-clang/` are optional self-hosted copies, git-ignored; see Self-hosting) |

## The C++ compiler (not vendored)

C++ code widgets (`language: "cpp"`) compile in the browser with YoWASP Clang, the npm package `@yowasp/clang@21.1.4-3` (LLVM 21.1.4; Apache 2.0 with the LLVM exception, which allows redistribution; the JavaScript wrapper is ISC). `js/engine/widgets/cpp-grade.js` loads it from `https://cdn.jsdelivr.net/npm/@yowasp/clang@21.1.4-3/gen/`; if that is unreachable, `js/screens/cpp-worker.js` tries `vendor/yowasp-clang/` (absent from the repository; `tools/fetch-vendor.sh` fills it). Alternatively put the package's `gen/` files on any static host with CORS and change `CLANG` in `cpp-grade.js`. Expected files:

| File | Bytes | gzip | SHA-256 |
| --- | ---: | ---: | --- |
| `bundle.js` | 253,210 | 25,059 | `fa207d915b251642aef2cb6e07b762e1d9d55af12d6b8fd52bffe30dc824bcd0` |
| `llvm.core.wasm` | 72,690,007 | 22,019,646 | `4677de03b671ffc7a7c9fb9eae1b9318ed94fb98e47c4f28935ea41cd9410f5d` |
| `llvm.core2.wasm` | 37,626 | | `960c326eb9b5db7aedbc169540421587a2d3f3ff987e93d6ad5b4da43430ffd4` |
| `llvm.core3.wasm` | 5,458 | | `63680c043192abac4700bbda6a78e4c19b139fa086b1e872d1c6915d37a428a8` |
| `llvm.core4.wasm` | 787 | | `f544dc9cc46f88a0f22d1b839a4fb0853dce2d6e231d880bd19754c59a5a234d` |
| `llvm-resources.tar` | 29,603,840 | 4,320,732 | `87a8be5f079692dee3e01c419361f766e2664c4fc60e01278858a8470f3c87d4` |

The npm tarball (`https://registry.npmjs.org/@yowasp/clang/-/clang-21.1.4-3.tgz`, 26,386,607 bytes) has SHA-256 `9c082ea5cac9489966adbe381529bf13bde18646126e98b8b089d83f57fe5e27` and npm integrity `sha512-xeAA7iFvDZ/C32d/h/BDSpmxEZePnorpi+EfaORDWwJN3c9rFXHvUVoHb+alo8U8jNaxJMWBLLGecT55D/YQKA==`. For `tools/playthrough.mjs --local-cdn <dir>`, untar it into `<dir>/yowasp-clang-21.1.4-3/`. The worker replaces one slow file-write function in `bundle.js` at load (only when the text matches this version exactly), so a version bump needs a check that precompiled headers still build in seconds.

## Moving around: locked lessons

A lesson, level review or homework opens only when the levels it relies on are met (`requires` in each `course.json`; a later level with none relies on the level before it). A level is met when you pass its review, pass its topic exam or the stage test, or test out of it. Opening a lesson does not count, and nothing you have unlocked locks again. A level you have met, or started by finishing a lesson, stays open for its other lessons and its review.

- The course map draws a locked node with a lock. Tap it, or open its link (`#lesson/<course>/<lesson>`), to see the locked card: what is missing, grouped Stage, Topic, Course, then level or lesson, each with a count. Direct prerequisites come first; the rest sit in one collapsed line per stage. "Start here" opens the earliest missing lesson whose own prerequisites are met.
- Each missing level offers "Test out" (`#testout/<course>/<level>`): up to 6 items from that level's review, passed at the review's pass share. A miss lists the lessons to revisit and waits 24 hours.
- You, Settings, Study plan, "Strict prerequisites" (on by default): on hides "Open anyway"; off shows it, and You counts the levels opened early.
- Today and Learn pick only unlocked lessons. Prepare marks a blocked step with a lock and its first missing prerequisite. A met prerequisite you have not reviewed for 30 days shows a "Refresh" chip above the lesson's first screen.
- Saves from before gating are grandfathered once: every level whose lessons were all finished counts as met.
- Authors: `docs/AUTHORING.md` section 11. The playthrough marks a target's prerequisites met before it plays (`ZQ.prereq.unlock`).

## Docs

- `docs/PLAN.md`: the build contract (runtime, state model, content model, engine, screens).
- `docs/AUTHORING.md`: how to write lessons, reviews, homework, exams and drills, and the rules the validator enforces.
- `docs/curriculum.md`: the curriculum the app teaches.
- `docs/design-research.md`: the design language, motion, lesson anatomy and voice.

## Learner data

Everything the learner does is one JSON document in this browser's `localStorage` under `zq.state`. Export and import it from the You screen; clearing site data resets the app.
