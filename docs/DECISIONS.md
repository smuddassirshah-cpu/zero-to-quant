# Decisions

The Phase 2 decision log (`docs/PLAN.md` section 10): the owner's decisions at Blueprint review, raw-HTML sink justifications, waivers of the engineering floor, spike results, dependency notes and every decision a build stage makes. `PLAN.md` section 12 states the options the owner chose between; this file records what was decided and everything decided after it.

Each entry gives the decision, the reason, the alternatives rejected and whether it departs from `PLAN.md`. Entries are never edited after the fact: a later decision that changes one adds a new entry naming the one it replaces. `STATE.md` keeps a one-line copy of each.

## 1. The owner's decisions at Blueprint review, 7 October 2026

These win over anything earlier in the documents (`PLAN.md` revision 2 note).

### D1 Build order: option (a)

- **Decision.** The engine and every P0 widget batch (stages 1 to 83) are built before any content; content then proceeds depth-first in curriculum order from 0.1 (stages 84 to 100, then Stage 1 by the same rule).
- **Reason.** The owner's priority: the best possible content engine and widget library first, so every later lesson has the best foundation. The Stage 1 prototype showed where defects live: its hand-built lesson took 1,316 lines of JavaScript for 12 minutes of learning and still had 23 review defects, mostly in timers, state and XP machinery.
- **Rejected.** (b) A companion release first (planner, outside-work log, Redo queue, Daily 10, weekly problems and Bertie from about March 2027, the library after); (c) content starting where the learner will be when stage 83 ends (1.1), with Stage 0 backfilled by a fifth session; (d) Stage 0 content after stage 41.
- **Consequence.** Content meets the learner about November 2028, late in 1.5 [our estimate, `PLAN.md` 11.2]; until then he studies from the canonical resources the item files name. The stage 28 re-forecast lever stands: below 15 AD a week, a fifth session is added or the owner is asked whether to revisit this decision.
- **Deviation from `PLAN.md`.** No.

### D2 Curriculum additions: the recommended set, adopted

- **Decision.**

  | Addition | Hours | Where |
  |---|---|---|
  | P1 Research method | 35 | Item 2.2c, Stage 2, immediately before 2.3 Projects |
  | P2 Continuous-time processes | +15 | Inside 1.5 Probability (levels Z4b and Z4c) |
  | P3 Numerical methods, floating point and Monte Carlo | 120 | Item 2.0a, first item of Stage 2, all tracks |
  | P4 Optimisation | 80 | Item 2.0b, after 2.0a and before 2.1 |
  | O1 Contests offset | $-80$ | From 2.4, outside the developer track |
  | 2.1b Deep learning core | 120 | New Stage 2 item after 2.1, all tracks |
  | A1 Real analysis | 60 | After 1.3, on the researcher and ML research tracks |

  Totals: 3,390 mapped hours on the trader track, 3,450 on the researcher and ML research tracks, 3,470 on the developer track [computed, `docs/CURRICULUM.md` header]. Proposals P5 to P16 are not adopted. P8 (differential equations) is among them, so every item file that listed P8 as a prerequisite teaches the basics it needs itself. The ML-lab aim of `PLAN.md` section 1 stays.
- **Reason.** Without 2.1b the stated aim of ML-lab-calibre thinking is not delivered; the subjects of P1 to P4 are core in every programme `docs/blueprint/work/canon-gap.md` surveys.
- **Rejected.** No additions, with the ML-lab aim dropped; every proposal (3,565 to 3,820 h by track); P5 to P16 one by one.
- **Effect on the build.** Stage 3g (`@zq/models/analysis`), batch W5d (stage 51a, A1's six scenes), 14 P0 modes on existing widgets, and P2 widgets and services for 2.0a, 2.0b, 2.1b and 2.2c in the first Stage 2 waves (`PLAN.md` 12, consequences table). No engine contract changes and no Artifact file beyond course bundles.
- **Deviation from `PLAN.md`.** No: `PLAN.md` revision 2 and the curriculum files carry it.

### D3 Brainy Bertie: confirmed, with rounded hair

- **Decision.** Bertie is confirmed as drawn in `docs/BERTIE.md` draft 2 except the hair, which becomes less spiky, more rounded and fuzzy: soft cloud-like tufts, not points. The owner's words: "Make his hair less spiky, more rounded and fuzzy. Everything else about Bertie is perfect." `docs/BERTIE.md` draft 3 (decision 16) redraws the hair and nothing else: twelve tufts that swell from a narrow root to a round, scalloped end, merged into one outline, with the flare at the upper corners and two flyaway wisps keeping the wild shock. Measured at 11,067 bytes gzipped against the 12,000-byte budget.
- **Reason.** The owner found draft 2's pointed locks too spiky.
- **Rejected.** Draft 2's flame-shaped locks; an even ring of round puffs, which reads as an afro [measured]; tufts with individual outlines, which show every root as a seam.
- **Open.** The owner signs off draft 3's hair at stage 59, before Bertie's visual baselines are committed.
- **Deviation from `PLAN.md`.** No.

### D4 Every other decision of `PLAN.md` section 12 at its stated default

| `PLAN.md` 12 | Decided |
|---|---|
| 3 Curriculum decisions D1 to D8 | As each item file recommends (`docs/CURRICULUM.md` 6.3) |
| 5 Sealed answer key | `sealed` on the web; on the Artifact, `sealed` only for the model tiers that pass the judged tier run, `never` for any that fails (`docs/AI-TUTOR.md` 9.6) |
| 6 Cloudflare plan for the limiter | Whichever plan offers SQLite-backed Durable Objects, checked at stage 62; the paid plan if the free plan lacks them |
| 8 Copyright and writing rules | The adapted-problem rule of `CONTENT-FORMAT.md` 9.4 as written; the glossary exemption for standard terms containing a banned word allowed; no public release, so the content licence waits until something is to be public |
| 9 Weekly hours split | 9/3/2/1 with up to 1 hour of borrowing from Main |
| 10 People outside the app | Both, paid: a person marks one finals-style sitting per Stage 1 maths topic (1.3, 1.4, 1.5, 1.6); a reviewer with a degree in the subject spot-checks 5 lessons per course from Stage 1 |
| 11 Reliance check | On, with a Settings switch |
| 12 Earlier habits | Off |

- **Reason.** The owner took the stated defaults at review.
- **Deviation from `PLAN.md`.** No.

### D5 The Artifact publishing rule

- **Decision.** The Artifact publishing tool requires the publishing session to read every file it did not write before publishing it, and a file it cannot read is never published. The Artifact therefore publishes **only files generated from this repository's own sources**: our compiled app code, content bundles, generator modules, our CSS and data. It publishes no third-party code and no binary. Third-party JavaScript loads at run time from cdnjs.cloudflare.com (preferred), cdn.jsdelivr.net/npm/ or unpkg.com at exact pinned versions, through an import map written from `cdn.lock.json`; fonts come only from Google Fonts. Consequences:
  - no Python, no SQLite WebAssembly, no KaTeX font files and no other third-party binary in the Artifact;
  - maths in the Artifact renders as MathML (KaTeX from the CDN with `output: 'mathml'`, in system maths fonts); MathLive is web only;
  - every Python, SQL and C++ drill in the Artifact hands off to the web app and returns by result code; lessons are unaffected, because authored code runs at build time;
  - the web app (GitHub Pages or local; where it is served before a content licence exists is `PLAN.md` 12 decision 13) is not published through the Artifact tool and keeps Pyodide with every load group, SQLite and KaTeX fonts;
  - `tools/pysplit`, the JSON-part layout, its release budgets and spike items are removed; the Artifact budget is about 198 files and 125 MB a release [our estimate, `ARCHITECTURE.md` 6.2.5];
  - stage 2's spike verifies on the owner's iPhone: CDN script and ES-module loading on the page and inside workers (or that workers use only our own code), the import map and its integrity, MathML rendering quality, and the `db`, `sample` and `user` behaviours.
- **Replaces.** Draft 1's decision 7 (questions to Anthropic about publishing repackaged binaries), the JSON-part Python layout and fallbacks F1 and F2.
- **Reason.** The tool's read-before-publish requirement: no session can read a third-party binary, so none can publish one.
- **Rejected.** Pyodide in the Artifact as JSON parts of wheel members (measured working on the owner's iPhone, but it publishes third-party binaries); MicroPython with `ulab` (a third-party binary); bundling third-party JavaScript into the Artifact's own files; jsDelivr's `+esm` builds, which resolve dependency ranges on the CDN; MathML emitted at build time, a second rendering path beside the run-time one that generated items, live formulas and Bertie's replies need.
- **Deviation from `PLAN.md`.** No: `PLAN.md` revision 2 (section 4.3 and conflicts 2, 8, 9, 12, 20 to 22) carries it.

### D6 The probe Artifacts: delete them

- **Decision.** The published probe Artifacts of Stage 1 (`spikes/artifact-probe`, `spikes/pyodide-in-artifact`) are to be deleted. Neither was found in the owner's Artifact listing (scope: mine, the default; an Artifact published from another session or organisation may not appear in it) on 7 October 2026 [measured], so nothing has been deleted yet. `spikes/` keeps their sources, and `spikes/README.md` their results, as the record.
- **Open.** If either probe is found (a listing with scope `all` or `shared`, or a link the owner holds), a session deletes it with the owner's confirmation and records the date here (`STATE.md` open question 22).
- **Done, 7 October 2026.** Both probes were found by their links and deleted with the owner's confirmation: `claude.ai/artifact/AVT67jiX14bVKkEFpTrbXN` and `claude.ai/artifact/S3wMgZk7sttLXR2AfZAwkG` [measured: the tool confirmed each deletion]. Open question 22 is closed.
- **Reason.** The owner's instruction; the measurements are recorded and neither runtime is adopted.
- **Deviation from `PLAN.md`.** No. Stage 2's own probes are published fresh, and its `db` size probe is deleted after its run with the owner's confirmation.

### Owner decisions raised by the second review round of `PLAN.md`, 7 October 2026

O1 and O2 below are the options as raised; D7 and D8 record what the owner decided at the Blueprint approval the same day.

- **O1 (`PLAN.md` 12 decision 13): where the web app is served before a content licence exists.** Options: (a) GitHub Pages, unlisted but world-readable, which counts as public, so the content licence and the `CONTENT-FORMAT.md` 9.4 sign-off come before stage 25's first deploy; (b) Cloudflare Pages behind a Cloudflare Access policy admitting only the owner's account, until he chooses a licence, with GitHub Pages kept as the public-release path; (c) local only. Recommended and default: (b), needed by stage 25. Reason: decision 8's default (no public release, D4) rules out (a), and (c) breaks the phone handoff the Artifact's drills depend on. The repository is private [measured, GitHub REST API, 7 October 2026].
- **O2 (`PLAN.md` 12 decision 14): the Stage 3 Zhou exit line.** Options: (a) `3.3.zhou` stays at Zhou chapter 4 logged cold at 80%; (b) canon-gap 4.4's line with P2, chapter 4 at 80% and chapter 5 at 70% cold. Recommended: (b), since P2 was adopted (D2) and 3.3 level PZ6 teaches chapter 5's material to every learner. Default: (a) until the owner confirms, needed before the 3.3 wave is briefed.

### D7 Where the web app is served before a content licence: option (b)

- **Decision.** The owner, at the Blueprint approval ("CloudFlare is fine"): every deployed web build is served from Cloudflare Pages behind a Cloudflare Access policy that admits only his account, until he chooses a content licence. `serve:web` stays the local path. GitHub Pages becomes the public-release path, used only after the licence decision and the Class D review of `PLAN.md` 7. Replaces O1.
- **Reason.** The only option that keeps decision 8's "no public release" (D4) and the phone handoff every Artifact drill depends on.
- **Rejected.** (a) GitHub Pages, unlisted but world-readable, which counts as public; (c) local only, which breaks the handoff away from the owner's network.
- **Open.** Access's free-plan terms (up to 50 users [recalled, unverified]) are checked at stage 25, the first deploy; the Access session lifetime against the service worker's update checks is [unverified] until stage 82 (`PLAN.md` 9).
- **Deviation from `PLAN.md`.** No: it is decision 13's default.

### D8 The Stage 3 Zhou exit line: option (b)

- **Decision.** The owner, at the Blueprint approval ("Add in chapter 5"): Zhou chapter 5 joins the Stage 3 exit at 70% solved cold, as a new exit part `3.3.zhou-ch5` (a `book-log` gate of chapter 5 at 0.7 in the learner's own copy, 7 hours moved out of `3.3.books`, now 54.5 h). `3.3.zhou` is unchanged: `exm.iv.zhou-cold` at 80% and the chapter 4 book-log at 80%. `docs/curriculum.md` gains the fourth 3.3 checkbox on his instruction. Replaces O2.
- **Reason.** P2 was adopted (D2): 1.5 levels Z4b and Z4c and 3.3 level PZ6 teach chapter 5's processes and Itô's formula at interview depth to every learner, so the exit measures what the path teaches.
- **Rejected.** (a) Chapter 4 alone; folding chapter 5 into `3.3.zhou` as a second confirm instrument, which would hide a separate curriculum line inside another part (`ASSESSMENT.md` decision 1: one exit part per curriculum exit line); an in-app cold set for chapter 5, which would add a second held-out pool of recreated problems for 7 hours of reading [our choice].
- **Edited.** `PLAN.md` 12; `docs/curriculum.md`; `docs/CURRICULUM.md` 3.1, 4.2, 4.3, 6.2, 6.3, 6.4; `ASSESSMENT.md` 2.9; `docs/curriculum/stage3-stochastic-interview.md` (revision 2 row, 3.0, 4.4, the outcomes, the reading rows). The exit data itself is written at stage 78 (`STATE.md` pending edit 4).
- **Deviation from `PLAN.md`.** No: it is decision 14's recommended option.

## 2. Raw-HTML sinks

The engineering floor requires a written justification for every raw-HTML sink. There are exactly two (`PLAN.md` 7.2, `ARCHITECTURE.md` 11.3); a third needs the owner's approval and an entry here before it is written.

### S1 KaTeX output in `src/engine/render/Tex.tsx`

- **What.** `Tex.tsx` sets `innerHTML` to the string `TexService.html()` returns: KaTeX 0.19.0's output, HTML with MathML on the web and MathML alone in the Artifact (`ARCHITECTURE.md` decision 37), from a least-recently-used cache of 1,000 entries.
- **What reaches it.** Only KaTeX's output, from two sources in two configurations of one sink (`PLAN.md` conflict 10):
  - authored TeX (trusted content, also rendered by the compiler's check): strict mode, macros from `content/tex-macros.yaml`, and a `trust` callback that allows only `\htmlData` with a name matching `^[a-z][a-z0-9-]{0,15}$`, for term anchors on the web. `TexSlots` does not use `\htmlData`: on both outputs each slot is a sentinel `\text{}` token; on the web its HTML span's text node is bound, and in every MathML tree the sentinel `<mtext>` is replaced by an `<mn>` built with `createElementNS` (a DOM node, not a sink) whose `textContent` follows the slot (revised before the gate by the second review round of `PLAN.md`);
  - maths spans in Bertie's replies (model output, untrusted): `trust: false`, `strict: 'ignore'`, `maxSize: 10`, `maxExpand: 1000` (`AI-TUTOR.md` 8.8).
- **Why it is acceptable.** KaTeX escapes its input and uses no `eval`; with `trust` off, or limited to `\htmlData` with a checked name, KaTeX refuses `\href`, `\url`, `\includegraphics` and the other `\html` commands [recalled; the stage 23 corpus tests it]; nothing but KaTeX's return value is ever assigned. On the web the CSP blocks inline script and every outside host but the proxy.
- **Tests.** Stage 23: a KaTeX injection corpus (`\href` with a script URL, `\htmlData` with a bad name, raw HTML in text) renders inert in both outputs. Stage 60: the tutor's Markdown renderer never produces an element outside its allow-list (property test).
- **Enforcement.** `zq/no-inner-html` bans `innerHTML`, `outerHTML`, `insertAdjacentHTML` and `dangerouslySetInnerHTML` everywhere except this file.
- **Rejected.** A second sink for Bertie's maths, which two trust settings of one sink make unnecessary; MathML emitted at build time (decision 37).

### S2 Bertie's rig markup in `src/ui/bertie/markup.ts`

- **What.** `svgMarkup(lod, id)` builds Bertie's SVG template from the module's own numeric constants and class names and parses it with `DOMParser` as `image/svg+xml`; the bolt is built with `createElementNS` (`BERTIE.md` decision 19).
- **What reaches it.** No data: no content, config, learner text or model output. The arguments are a level-of-detail value and an instance id from a counter the module owns, used for per-instance clip-path ids (`bz<n>-eye-l`).
- **Why it is acceptable.** The template is a module constant, and parsing it as SVG keeps the HTML parser out entirely. Bertie's speech goes through `say()`, which sets `textContent` only; `say('<img src=x onerror=...>')` renders the literal text and creates no element [measured, `BERTIE.md` 12.2].
- **Enforcement.** `PLAN.md` 7.2 puts both sinks under `zq/no-inner-html`, but `ARCHITECTURE.md` 10.4 lists only the `innerHTML` family. Stage 1 extends the rule to `DOMParser.prototype.parseFromString` and `Range.prototype.createContextualFragment` outside `src/ui/bertie/markup.ts`, so a planted call elsewhere fails lint. Not a deviation: `PLAN.md` wins over the appendix, whose row is updated at stage 1.
- **Rejected.** `innerHTML` on a `div` with the same constant markup.

## 3. Waivers

### W1 The tutor token is a credential stored in the browser

- **Floor rule waived.** "No credentials in localStorage"; the session-cookie pattern.
- **What.** On the web app, `TUTOR_TOKEN` is entered once per device in Settings and stored in IndexedDB through `KeyValue.setSecret`, never `localStorage`; it travels as a bearer header to the proxy (`PLAN.md` 7.1 and 7.2).
- **Why.** The static web front end (on the host of `PLAN.md` 12 decision 13) and the Cloudflare Worker are different sites, which rules out a first-party httpOnly cookie.
- **Compensating controls.** The token can only spend on the tutor, within USD 3 a day and USD 30 a month and the request limits of `PLAN.md` 7.3; the web app's CSP limits `connect-src` to its own origin and the proxy; no model output or learner text reaches an HTML sink (S1, S2); the token is never logged and never shown again after saving; rotation is one `wrangler secret put`. The Artifact holds no tutor token: its tutor runs on the viewer's own account through `sample`.
- **Expires.** The day another learner is admitted (Class D). Upgrade path: the proxy as a same-origin Pages function beside the front end on Cloudflare Pages, and an httpOnly session cookie.

### W2 Third-party modules in the Artifact without guaranteed subresource integrity

- **Floor rule affected.** Supply-chain integrity of shipped code. Versions stay pinned and the lockfile committed; what cannot be guaranteed is that the browser checks the bytes.
- **What.** Under D5 the Artifact loads Preact, `@preact/signals`, `zod/mini`, `idb`, `ts-fsrs`, KaTeX, the Compute Engine parser, MiniSearch and, in the data worker, classic zod, ts-fsrs and fflate from cdnjs or jsDelivr. The import map's `integrity` field may not be enforced on iOS 18.7 [unverified; stage 2], and worker imports carry no integrity at all.
- **Exposure.** Altered bytes from a CDN could read the viewer's progress, write their `db` subtree and call `sample` on their account; the host's CSP lets them reach no host beyond the listed CDNs [inferred] (`PLAN.md` 7.4).
- **Compensating controls.** Exact-version URLs only, from `cdn.lock.json` with each file's SHA-384 (never a range, `@latest` or `+esm`); `integrity` on every import-map entry, enforced wherever the browser does; a nightly job that refetches every locked URL, fails on any byte difference and blocks Artifact releases until the file is re-pinned; `tools/release/provenance.ts`; the web app bundles everything and loads nothing from a CDN.
- **Review.** At stage 2: if the page enforces import-map integrity, this waiver narrows to worker imports; if workers cannot import from the CDN hosts, the data worker's jobs move to the main thread and the worker part lapses. Redone before any Class D release.

## 4. Spike results

### Stage 1 (design) probes, 6 October 2026: recorded, not adopted for the Artifact

Details in `spikes/README.md`. Both ran as private Artifacts on the owner's iPhone (iOS 18.7, Claude app).

- **artifact-probe.** Every check passed except service workers, which are absent: WebAssembly on the page and in a worker, fetching published `.json` and `.wasm`, classic and blob workers, MicroPython with `ulab`, browser storage, and the `sample` (quick tier; page tools up to 16; no image input in that view), `db` and `user` capabilities. The capability, storage and worker results are used by the plan; the WebAssembly and MicroPython results are a record only (D5).
- **pyodide-in-artifact.** Python 3.14.2 ready at 2.8 s, NumPy and pandas loaded at 5.1 s, a drawdown computed correctly at 6.2 s, through archives split into served file types. Measured, not adopted (D5): it publishes Pyodide's binaries. The timings remain the plan's reference for Pyodide on that phone until stage 25 measures the web app.

### Spike S1 (stage 2)

Pending. Record each check with device, app version and date, the import-map verdict (section 4.3's design or its named fallback) before stage 4 starts, the MathML verdict with screenshots, and the `db` size probe's result.

## 5. Dependencies, licences and advisories

A new dependency adds an entry: name and exact version, maintained, last release, licence, why, and the date of the owner's approval. Licence exceptions beyond the allow-lists of `PLAN.md` 7.6, and advisory waivers past a week, are entered here with their reason. `tools/ci/licences.exceptions.json` and `tools/ci/audit-waivers.json` name these entries; an exception that matches nothing or a waiver past its date fails CI. Stage 1 recorded L1, A1, A2, T1 and G1 for the owner's review at its gate.

### L1 Licence exceptions for four of stylelint's dependencies (stage 1)

- **What.** Development only, all through `stylelint` 17.16.0: `svg-tags` 1.0.0, whose `license` the lockfile does not record (it declares MIT in the legacy `licenses` array and ships an MIT `LICENSE` file), and `@csstools/css-syntax-patches-for-csstree` 1.1.15, `@csstools/selector-resolve-nested` 4.0.2 and `@csstools/selector-specificity` 6.0.1, which are MIT-0 [measured, `package-lock.json` and the installed packages, 7 October 2026].
- **Why.** MIT-0 is MIT without the attribution condition, so it asks less of us than MIT; none of the four ships to learners.
- **Rejected.** Adding MIT-0 to the development allow-list, which would change `PLAN.md` 7.6; replacing stylelint, which `PLAN.md` 4.2 pins.

### A1 Advisory waiver: `braces` 3.0.3, GHSA-vfj7-8cjw-p6xm, until 7 November 2026 (stage 1)

- **What.** npm audit rates it high: stack exhaustion through deeply nested brace patterns. Development only, through `stylelint` 17.16.0 and `micromatch` 4.0.8. No fixed `braces` exists: 3.0.3 is its latest release [measured, npm registry, 7 October 2026].
- **Why.** Exploitation needs an attacker to choose the glob pattern; stylelint expands only the patterns in our own scripts and config.
- **Rejected.** Moving stylelint or overriding `braces`, both pin changes the owner approves; failing every pull request on an advisory nobody can fix.
- **Review.** When `braces` or `micromatch` publishes a fix, or at expiry.

### A2 Advisory waiver: `pytest` 9.0.2, GHSA-6w46-j5rx-g56g (CVE-2025-71176), until 7 November 2026 (stage 1)

- **What.** pytest up to 9.0.2 uses predictable `/tmp/pytest-of-<user>` directories, which lets another local user on a UNIX machine cause a denial of service or possibly gain privileges; 9.0.3 fixes it [measured, PyPI advisory data, 7 October 2026; severity unverified].
- **Why.** `PLAN.md` 4.2 pins pytest to Pyodide 314.0.7's lock, which has 9.0.2, so drills are graded in CI against the version the web app loads. CI runners and the owner's machine are single-user, and Pyodide has no shared `/tmp`.
- **Rejected.** pytest 9.0.3 in `tools/py/uv.lock`, which departs from the Pyodide pin and is the owner's call.
- **Review.** At the owner's stage 1 gate, when Pyodide's lock moves past 9.0.2, or at expiry.

### T1 Stage 1's CI tools outside the npm tree (stage 1)

- **gitleaks v8.30.1.** MIT [measured, the module's `LICENSE`]. Maintained: released 21 February 2026, the latest version on the Go module proxy on 7 October 2026 [measured]. `go install` builds it into the ignored `.zq/bin`; sum.golang.org verifies the module and `tools/ci/gitleaks.ts` checks the binary against its pinned module hash. Never vendored or published.
- **pip-audit 2.10.1.** Apache-2.0 [measured, PyPI classifier]. Maintained: released 10 June 2026, the latest on PyPI [measured]. In the `dev` group of `tools/py/uv.lock`; it runs in CI and before a push only.
- **Go toolchain floor.** gitleaks v8.30.1's `go.mod` declares go 1.24.11 [measured]. CI pins `setup-go` to go 1.26.8, the toolchain `GOTOOLCHAIN=auto` fetched for this build [measured]; an older local Go fetches a newer toolchain through the module proxy, verified by sum.golang.org.
- **Why.** `PLAN.md` 7.1 and 7.6 name gitleaks and pip-audit, so they came with the Blueprint's approval; the exact versions are for the owner's review at the stage 1 gate.
- **Licence scope.** Stage 1's licence gate covers the npm tree only. The Python lock is CI tooling and holds licences outside the development allow-list, pillow 12.3.0 (MIT-CMU) and typing-extensions 4.16.0 (PSF-2.0) [measured, PyPI]; Python packages are checked at stage 25, when Pyodide's packages ship on the web app. No Python licence gate is built before then.

### G1 The label guard checks who applied `visual-approved` and that it postdates the head commit (stage 1; departs from `PLAN.md` 7.1; for B5)

- **What.** `PLAN.md` 7.1 has `label-guard.yml` check the label against the owner's approval review. It checks instead that the latest `labeled` event for `visual-approved` came from the owner's account, applied directly rather than through a GitHub App, after the pull request's head commit arrived. `tools/ci/label-guard.ts` binds the label to the head commit: the label must be later than the earliest `created_at` of that commit's check suites, which GitHub sets and the pusher cannot, and a missing time fails; it also fails if a force-push followed the label. The workflow removes the label on every push and reopening (`synchronize`, `reopened`) and fails that run, so the check stays red until the owner labels the new head. It has no concurrency group, because GitHub cancels a pending run when a newer one joins the group, even without `cancel-in-progress`, which would let a label toggle cancel the run that removes the label.
- **Why.** The pull requests are opened by the owner's own account [measured: the session platform's GitHub connection authenticates as `smuddassirshah-cpu`], and GitHub refuses an approving review from a pull request's author [recalled], so the review the plan names can never exist.
- **Where it runs.** On `pull_request_target`, from base-side code only, because on `pull_request` the workflow comes from the pull request's own merge commit, which the pull request could rewrite. Which branch `pull_request_target` reads the workflow from, the base or the default branch, is [unverified]; the guard is binding once it is on `main`.
- **Limit.** The guard refuses every other account but cannot tell an agent acting through the owner's connection from the owner; that rule stays procedural (`CLAUDE.md` hard rule 3).
- **Rejected.** The approval review (impossible here); the guard on `pull_request` (rewritable by the pull request it judges); comparing the label with commit dates, which the pusher sets.

## 6. Build decisions

None yet. Each stage adds its decisions here in the format above, numbered B1 onwards, with the stage that made them. Stage 14 records the scene layer's go or revert decision per family here.
