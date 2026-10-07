# Brainy Bertie: mascot design and rig

> **Appendix to `docs/PLAN.md`.** Moved from `docs/blueprint/work/bertie.md` on 7 October 2026 and tidied for the blueprint. Section numbers are unchanged. `docs/PLAN.md` wins where the two differ. Tidied in place: section 12.1's files are TypeScript, and the spring integrator lives in `src/engine/motion/spring.ts`, shared with widgets (`ARCHITECTURE.md` 0.3). The budget of section 9 (12,000 bytes gzipped) applies to the TypeScript build output.

Blueprint work file, Stage 2 Phase 1. Draft 3, 7 October 2026 (hair only); draft 2, 6 October 2026.

**Draft 2** keeps every section number of draft 1, because `AI-TUTOR.md` cites sections 0, 5, 7, 10 and 12. It is a second art pass on the same rig: a new hair construction, a hairline cut into the face, eyelids, a visible smile and a tighter small cut. The API, the state set, the springs and the motion rules are unchanged. Section 0.3 lists every change and its reason.

**Draft 3, 7 October 2026 (change note).** At the blueprint review the owner confirmed Bertie as drawn except the hair: "Make his hair less spiky, more rounded and fuzzy. Everything else about Bertie is perfect." Draft 3 redraws the hair and nothing else. Draft 2's pointed flame locks become soft, rounded puffs with gently scalloped edges, flaring up and out at the upper corners, with two shaded back puffs behind the crown and two flyaway wisp puffs. The face and hairline, eyes, lids, brows, moustache, mouth, jumper, bow tie, colours and tokens, rig groups and names, states, springs and motion timings are unchanged. Section numbers are unchanged; section 0.4 lists every change and its reason, and sections 0.1 (decisions 2, 14 and 16), 0.2, 1, 2.1 to 2.4, 2.6, 3, 4.1, 4.2, 5.1, 9, 11, 12 and 13 carry it.

**Scope.** The art and animation of Brainy Bertie, the Zero to Quant mascot and the face of the AI tutor: construction (section 2), the SVG rig (3), the motion system (4), states and their triggers (5), reduced motion (6), where he appears (7), accessibility (8), performance and the size budget (9), the JavaScript API (10), the rendering technology decision (11), build layout and tests (12) and open questions (13). It is the art authority that `AI-TUTOR.md` (decision 25, sections 3.2 and 7.2) defers to.

**Prototype.** `prototype/bertie.html` is the working rig: every state, sizes 32, 40, 48, 64, 96 and 160 px beside a 220 px stage (180 px on a phone), in-context mocks (verdict bubbles, dock, map marker, exam bar, rest day), a speech-bubble demo with streaming, pointer gaze, a theme toggle and a reduced-motion toggle. Its first `<script>` block and the `bertie.css` block are the production component, written to be lifted verbatim into the build (section 12).

**Read for this file.** `docs/design-research.md` sections 1, 3 (character), 4 (motion), 6 and 7.4; `prototype/css/tokens.css` and `components.css`; `docs/AI-TUTOR.md` decision 25 and sections 3.2, 7.1 to 7.8; `spikes/README.md` (the Artifact probe); the platform facts in the Stage 2 brief; the engineering floor (`project-forge/references/engineering-floor.md`).

**Evidence tags.** [measured] for values read from the prototype in Chromium on 6 October 2026; [sourced] for facts from the brief's platform list, `spikes/README.md` or another cited file; [recalled, unverified] for general knowledge not re-checked here; [our choice] marks a decision where no evidence applies. Untagged statements are rules this file sets.

---

## 0. Decisions in brief

### 0.1 Decisions

| # | Decision | Chosen | Rejected | Reason |
|---|---|---|---|---|
| 1 | Rendering | Inline SVG. A small spring integrator on `requestAnimationFrame` drives the neck and hair; CSS transitions drive pose channels; Web Animations drive timed effects | Rive; Lottie (`lottie-web`); canvas 2D; sprite sheets; CSS keyframes only | Section 11. In short: Rive's default runtime fetch is blocked in the Artifact and the alternatives cannot do live physics, gaze or per-delta speech, or cannot take theme tokens |
| 2 | Recognisability | Caricature of the wild-haired professor archetype: a high bald dome, white hair swept up and out sideways in soft, rounded puffs, a hairline that comes down to a point above each ear, a bushy walrus moustache, a round nose, kind lidded eyes, heavy brows | A likeness of a real person; a non-human mascot | The owner asked for an Einstein-style bobble head. The bald dome inside a wide white halo, plus the moustache, carries recognition at 32 px; nothing in the art copies a photograph |
| 3 | Levels of detail | Two cuts from one rig: **small** below 80 px, **large** from 80 px | One drawing scaled to every size; three cuts | One scaled drawing fails at 32 px: wisps turn to noise and brows merge with eyes [measured, draft 1]. Two cuts cover 32 to 220 px |
| 4 | Outline | One warm-ink outline, size-aware: $w_{\text{px}} = \operatorname{clamp}(\text{size}/70,\ 1.25,\ 2.6)$. The hair has one merged outer outline (decision 16) | No outline; pure black `#000000` | White hair on a white canvas has no edge without a line. Warm ink `#2A2420` is softer than black against peach skin and still 15.3:1 on white [measured] |
| 5 | Colours by theme | Character colours fixed in both themes; only the ground shadow changes | Theme-inverted character | A character does not invert. White hair on the dark canvas is 18.4:1 and needs no help [measured] |
| 6 | Brand colour on Bertie | One accent: a pear bow tie (`--pear-400`) | No brand colour; a pear jumper | Brilliant puts pear on the streak bolt and the mascot (design research, finding 27). A bow tie is a small mark that cannot be mistaken for the streak bolt. The `tokens.css` comment "Brand pear (streak only)" becomes "streak and Bertie's bow tie" |
| 7 | Bobble mechanism | A hidden neck spring: a plain skin neck (`g.neck`), with physics on the head group about a pivot under the chin | A visible coil spring | A coil reads as a jack-in-the-box or a robot and adds a part that turns to noise below 64 px. The hop in `celebrate` still shows the neck stretch, because the head rises off the neck [measured, filmstrip] |
| 8 | Arms | None. Pointing is a head tilt, a nudge and a glance | Small arms or hands | Arms add six parts and two states each, read badly at 32 px, and Brilliant's Koji manages without them |
| 9 | State set | 10 held states and 4 one-shots (section 5), with aliases for the names `AI-TUTOR.md` uses | The tutor's 9 states only | The brief adds correct, celebrate, streak, sleeping, surprised and point; aliases keep both files valid |
| 10 | Not-yet face | Encouraging: inner brow ends raised, lids slanted down at the outer ends, a small smile, a sympathetic 6° tilt, then a nod | Knitted brows | Knitted brows read as disapproval. The owner asked for "not-yet encouraging"; the verdict copy already carries the bad news |
| 11 | Meaning | Bertie is always decorative (`aria-hidden="true"`); text carries every meaning | Bertie as an informative image | Matches `AI-TUTOR.md` 7.8: no state change carries meaning on its own |
| 12 | Name and likeness | Never called Einstein in copy, alt text or code comments shipped to users; never quotes anyone | Naming the character after the person | Consistent with `AI-TUTOR.md` 3.2. Rights in a famous person's name and likeness may be licensed commercially [recalled, unverified]; section 13 keeps the question open for any public launch |
| 13 | Speech bubble | `say()` renders plain text only (`textContent`) and keeps the bubble inside a bounding element | `innerHTML`; placement against the viewport | No raw-HTML sink (engineering floor). Viewport-based placement overflowed the stage at 1,280 px in draft 1 [measured]. Lesson verdict bubbles with KaTeX are the lesson player's component; `say()` serves onboarding, the map and the streak sheet |
| 14 | Size budget | 12,000 bytes minified and gzipped for the whole component (JS and CSS); 100 SVG elements per instance | No budget | Measured 11,067 bytes and 92 elements (section 9, draft 3) |
| 15 | Thinking signal | Three electrons on a dashed orbit around his head, in the hint indigo | Spinner; animated ellipsis | The atom reads as "working something out" rather than "loading" |
| 16 | Hair construction (draft 3) | Twelve soft tufts over a shaded scalloped mass: three front puffs a side (largest at the upper corners, tucked in by the ears), a crown puff a side, two back puffs filled with the hair shade that peek over the dome, and two flyaway wisp puffs. Each tuft swells from a narrow root to a round end, and its outer edge is a run of circular scallops. All of it is drawn twice: once as a line-coloured silhouette with a double-width stroke, then filled on top, so every overlap merges into one outer outline | Draft 2's twelve flame-shaped locks with pointed tips; draft 1's single flame-lobed ring with crescent strands; an even ring of round puffs; tufts with individual outlines | The owner found draft 2's points too spiky (review, 7 October 2026). Round ends with scallops read as soft fuzz; the flare at the upper corners and the flyaway wisps keep the wild shock; the back puffs give depth with an existing token. An even ring of round ends merges into one cloud, an afro [measured]. Draft 1's ring read as a crown of spikes [measured, contact sheet]. Individual outlines show every root as a seam ("paper petals", draft 1). The merged outline keeps one clean edge while each tuft still swings on its own spring |
| 17 | Eyelids | A skin-coloured lid inside each eye, clipped to the eye, with its own edge line. It has a closure (0 to 1) and a slant per pose; blinks drop it to shut | Draft 1's blink by squashing the eye to 8% height; no lids | The brief names lids in the rig. Lids give kind (outer ends down), sceptical (one lid lower) and sleepy faces without new shapes, and a lid blink keeps the eye's outline. At 32 px a lid blink still reads as a blink [measured] |
| 18 | Hairline | The face path carries the hairline: the dome narrows at the temples and comes down to a point above each ear, where the hair behind shows through | Temple locks drawn over the face and clipped to it; an egg-shaped face inside the hair | The hairline makes the head read as one object with wild hair, not an egg on a cloud. Clipped temple locks left an anti-aliased seam along the clip edge at 2x and 3x [measured] |
| 19 | Rig markup | Built from the module's numeric constants and parsed with `DOMParser` as `image/svg+xml`; no data reaches it | `innerHTML` on a `div` | The engineering floor requires a written justification for any raw-HTML sink. This template contains only numbers and class names written in the module; parsing it as SVG keeps the HTML parser out entirely. This row is the justification `DECISIONS.md` will carry |

### 0.2 Changes to `AI-TUTOR.md` section 7.2 (draft 1)

`AI-TUTOR.md` draft 2 (decision 25) now defers to this file, so this table records how this file departed from the tutor paper's first art notes.

| `AI-TUTOR.md` 7.2 draft 1 said | This file sets | Why |
|---|---|---|
| "a halo of 7 to 9 white hair strokes" | Ten rounded tufts (two of them back puffs in the hair shade) plus two wisp puffs over a shaded mass, one merged outline (decision 16, draft 3); seven broad puffs in the small cut | Separate strokes showed visible roots and read as petals or thorns [measured, draft 1] |
| "Flat fills from the neutral ramp, 2px ink strokes" | Character palette in section 2.4 (skin, jumper, bow tie are not neutral); size-aware outline of 1.25 to 2.6 px | Neutral-only fills made a grey ghost; a fixed 2 px line is too heavy at 32 px and too light at 220 px |
| `idle`: "hair sways 1° over 4 s" | Breathing bob, blinks, fidgets; the hair moves only through its springs | A constant sway on a still character looks like wind |
| `pleased`: "a single nod, 300 ms, spring-bounce" | `correct`: happy squint for 650 ms, a double nod from two spring impulses, a broad smile | A single 300 ms nod was too slight to notice at 32 px |
| `concerned`: "tilts 8°, brows knit" | `notyet`: 6° tilt, inner brow ends raised, sympathetic lids, small smile, nod at 480 ms | Decision 10 |
| Bobble: "`spring-physical`, 700 ms, at most 4°" | A damped spring, damping ratio about 0.31, settling in about 1.5 s; held tilts up to 9°, flicks briefly to about 15° | A fixed keyframe spring cannot be retargeted mid-flight without a jump; a live spring can (section 4.2) |
| Sizes: 32, 40, 64, 96 | 32, 40, 48, 64, 96, 120, 160, 220 (section 7) | The brief adds 160 px celebrations and the onboarding host |
| States | Adds `correct` (alias `pleased`), `notyet` (alias `concerned`), `celebrate`, `streak`, `sleeping`, `surprised`, `point` | Decision 9 |

### 0.3 Changes in draft 2

| Area | Draft 1 | Draft 2 | Reason |
|---|---|---|---|
| Hair | One flame-lobed mass (10 lobes) plus 4 outlined crescent strands | 10 locks and 2 wisps over a shaded mass, merged outline, each lock on its own spring | Decision 16. Draft 1 read as a spiky crown; the new halo is wider than tall and swept out sideways, the archetype's silhouette |
| Hair colour | White only | White locks over a hair-shade mass (`--bertie-hair-shade`, `#E4E1EA`) | The shade in the valleys gives the hair volume and stops gaps between swinging locks showing the page |
| Face | Ellipse $44 \times 50$ | Path with a high dome and a hairline that comes down to a point above each ear | Decision 18 |
| Eyes | $6 \times 8$ dots; blink by squash | $6.1 \times 8.1$ dots with lids; blink by lid | Decision 17. Slightly larger eyes read kinder at 160 px |
| Mouth | Hidden under the moustache when closed | A resting smile shows under the moustache (closure 0.25); opens downwards; tongue clipped inside the mouth | The smile is the cheapest warmth in the drawing, and an open mouth below the moustache reads at 96 px |
| Brows | $70 \to 90$, round strokes, minimum width $7\,u$ | $73 \to 91$, minimum $6.4\,u$ | Draft 1's brows touched the new hairline |
| Small cut | viewBox $(14, -2, 172, 172)$, 7 lobes, eyes ×1.3 | viewBox $(16, 10, 168, 168)$, 7 shorter locks, eyes ×1.2, shirt and shoulders fitted inside the frame | Draft 2's hair reaches further out; shorter small-cut locks keep the figure inside its box at 32 px |
| Markup | `innerHTML` with constant markup | `DOMParser` as SVG (decision 19); the bolt is built with `createElementNS` | Engineering floor |
| Budget | 9,978 bytes, 60 elements | 10,615 bytes, 92 elements; element budget raised from 80 to 100 | The merged outline draws the hair twice (26 elements) |

### 0.4 Changes in draft 3 (7 October 2026, hair only)

The owner's review note: "Make his hair less spiky, more rounded and fuzzy. Everything else about Bertie is perfect." Only the hair changed.

| Area | Draft 2 | Draft 3 | Reason |
|---|---|---|---|
| Tuft shape | Flame-shaped comma locks curling to a point (`lockPath`) | Rounded tufts (`tuftPath`, section 2.2): the half width eases from the root to a round end; past the root-most 40% of each side the outline is a run of circular arcs about 16 u long (22 u in the small cut), each bulging about a quarter of its length | The owner's note. Arcs keep the edge soft at every size and add no elements |
| Arrangement | Ten locks every 26° from 206° to −26°, plus two thin wisps poking out of the side wings | Three front puffs a side at 214°, 182° and 150° (mirrored), a crown puff at 126° and 54°, two back puffs at 102° and 78°, two wisp puffs at 198° and −18° | Round ends at an even 26° spacing touch and merge into one cloud, an afro with no tufts [measured]. Puffs that grow towards the upper corners and tuck in by the ears keep the archetype's flare |
| Back puffs | None | The two crown tufts at 102° and 78° are filled with `--bertie-hair-shade` and drawn before the white fills | White puffs in front of shaded ones read as volume and separate the tufts. An all-white crown read as a cloud helmet [measured]. No new colour: the token already shaded the mass |
| Wisps | Thin locks (half width 6 u) with pointed tips | Small round puffs (end radius 10 u) on short stems below the side wings; still the softest springs | Thin stems read as spikes, and through the crown as a white stripe [measured] |
| Mass | $70 \times 54\,u$, bulge 1.22 ($68 \times 54$ small) | $62 \times 48\,u$, bulge 1.18 ($58 \times 46$ small) | A mass as large as draft 2's filled the notches between round ends and merged the hair into a blob [measured] |
| Head with hair | $176 \times 135\,u$ | $188 \times 139\,u$; the small cut still fits inside its viewBox with no margin | Round ends carry more area to the sides than points [measured, `getBBox`] |
| Budget | 10,615 bytes gzipped | 11,067 bytes gzipped; elements unchanged (92 large, 74 small) | The outline resampling and arc code in `tuftPath` |
| Rig | `path.tuft[i]` and `path.tuft-l[i]`, 12 large, 7 small | Unchanged: names, groups, counts, pivots, springs, stiffness and limits. A back puff is `path.f-hair-shade.tuft` | The existing springs drive the new shapes with no change [measured, filmstrips] |

---

## 1. The character

- **Who he is.** A little cartoon professor in a slate jumper and a pear bow tie, all head: a high bald dome, wild white hair in soft puffs swept up and out to the sides, heavy dark brows, kind lidded eyes, a round nose and a big bushy moustache over a small smile. His personality is in `AI-TUTOR.md` 3.2: warm, curious, a little dry, never cute.
- **Design philosophy.** Brilliant's rule is "quiet canvas, loud boundaries" (design research section 1). Bertie follows it: during a problem he is still and small at the edge of the card; he gets energy only at boundaries (a verdict, lesson complete, a streak). A character "lowers the stakes" [sourced, design research 3]: a not-yet result comes with a kind face, not a red cross.
- **Recognition test.** At 32 px, with the face features blurred, the silhouette alone (a skin dome inside a wide white halo, above a small dark collar) should say "wild-haired professor". The prototype passes at 32 px, 1x, in both themes [measured: the 1x contact sheet, `#sizes` and the verdict chips].
- **Minimal detail.** In the large cut the eye sees 22 shapes: the hair silhouette, 2 ears, the face, 2 blush ovals, 2 brows, 2 eyes with 2 glints and 2 lid edges, the nose, 2 moustache halves, the mouth, the neck, the jumper, the shirt and the bow tie. No wrinkles, no irises, no hair texture lines (the scallops are the hair's edge, not lines inside it), no gradients, and no shading except the hair shade (the mass and the two back puffs) and one darker skin tone for the nose and neck.

---

## 2. Construction

### 2.1 Canvas and proportions

The rig is drawn in viewBox units (u). The large cut uses viewBox $(-8, -12, 216, 216)$; the small cut uses $(16, 10, 168, 168)$, cropped to head and shoulders.

| Part | Shape | Key geometry (u) |
|---|---|---|
| Face | Path | dome top $(100, 44)$; hairline corners $(67, 60)$ and $(133, 60)$; the hairline curves inwards to points at $(60, 96)$ and $(140, 96)$; jaw $x = 54$ to $146$; chin $y = 151$ |
| Ears | Ellipses, drawn under the face | centres $(54, 106)$ and $(146, 106)$, $8.5 \times 11.5$ |
| Eyes | Filled ellipses with a white glint (large cut) | centres $(82, 99)$ and $(118, 99)$, $r_x = 6.1$, $r_y = 8.1$; glint $r = 2.1$ at $(+2.1, -2.9)$ |
| Lids | Skin shape above each eye, clipped to it, with a curved edge line | edge from $y - 8.1$ (open) down by $12.6\,u$ (shut); resting closure 0.1; resting slant 6°, outer ends down |
| Brows | Quadratic strokes, round caps | left $73,89 \to 91,85$ through control $80,80$; right mirrored. Outer ends lower than inner ends: the resting face is kind |
| Nose | Ellipse, skin shade | centre $(100, 112)$, $9.5 \times 8$ |
| Moustache | Two mirrored halves, each with a scalloped lower edge (3 scallops) and a drooping tip | spans $x = 65$ to $135$, $y = 107$ to $138$; pivot $(100, 116)$ |
| Mouth | Smile-shaped top edge, round bottom, scaled vertically from its top edge | top $89,134 \to 111,134$ dipping to $y = 137$; full depth to $y \approx 147.5$; closure 0.25 is the resting smile |
| Neck | Rectangle, skin shade (`g.neck`) | $x = 88$ to $112$, $y = 128$ to $172$, mostly hidden; it shows as the spring lifts the head |
| Body | Rounded bust (large) or shoulder arc (small) | large: $x = 38$ to $162$, $y = 160$ to $200$, V-neck shirt, bow tie at $(100, 167)$; small: $x = 32$ to $168$, $y = 156$ to $178$ |
| Head pivot | Point | $(100, 150)$, under the chin, so tilts swing the top of the head like a bobble head |
| Hair centre | Point | $(100, 90)$ |

Proportions [measured, `getBBox`, draft 3]: the head with its hair spans $188 \times 139\,u$ ($x = 6$ to $194$, $y = 12$ to $151$); the large figure is $188\,u$ tall, so the head is 74% of the figure, the bobble-head ratio. The face is $92\,u$ wide, 49% of the hair's width, so the hair reads first and the face second. The small cut's hair spans $x = 20$ to $180$, $y = 18.5$ to $132$, inside its viewBox.

### 2.2 Hair geometry

The hair is generated from tables, so it is tuned by editing numbers rather than redrawing paths. Draft 3 (7 October 2026) replaced draft 2's pointed locks with rounded tufts; section 0.4 gives the reasons.

- **The tuft primitive.** `tuftPath(R, dir, len, w, curl, cap, chord)` draws one tuft from root $R$ in direction `dir`. Its spine runs $\text{len} - \text{cap}$ and bends steadily through `curl` degrees; the half width eases from $w$ at the root to the end radius $\text{cap}$ along the spine (smoothstep, $3q^2 - 2q^3$ for $q$ from 0 to 1); a half circle of radius $\text{cap}$ closes the end. The outline is then resampled into points about `chord` apart, and each pair is joined by a circular arc of radius $0.62 \times$ its chord (`SCALLOP`), which bulges outwards by about a quarter of the chord. The root-most 40% of each side stays straight (`PLAIN`): it lies behind the face or in a valley, where bumps would only add noise. The arc's sweep flag comes from the outline's winding, so every scallop bulges outwards whichever way the tuft points. Each tuft is one path: a narrow root, a full round puff, a gently scalloped edge.
- **Front puffs (large cut).** Three a side, roots 32° apart at 214°, 182° and 150° (mirrored at −34°, −2° and 30°), root radius 36 u, root half width 11 to 12 u, end radii 15, 20 and 23 u, lengths 31, 50 and 61 u. The upper-corner puff is the largest and reaches furthest, so the hair flares up and out like the archetype; the lower puff is short and tucks in by the ear. Curls of 12° to 22° lift every end upwards.
- **Crown puffs (large cut).** One a side at 126° and 54°: root radius 34 u, end radius 17 u, length 45 u.
- **Back puffs (large cut).** Two tufts at 102° and 78°, root half width 13 u, end radius 21 u, length 43 u, flagged `back` (the eighth table column). They are filled with `--bertie-hair-shade` and drawn before the white fills, so they read as hair behind the head, peeking over the dome between the white puffs. Both curl the same way (16° anticlockwise): one asymmetry, a cowlick, gives him character without breaking the balance.
- **Wisps (large cut).** Two flyaway puffs at 198° and −18°: root half width 5 u, end radius 10 u, length 56 u, curl 24° upwards. They sit below the side wings and keep the softest springs (stiffness 0.6 and 0.65, limit ±30°), so they swing widest.
- **Small cut.** Seven broad puffs at 208°, 172°, 132°, 90°, 48°, 8° and −28°: root half width 12 to 14 u, end radii 19 to 22 u, lengths 37 to 48 u, scallops 22 u long, so a bump is about 4 px at 32 px. The 90° puff is the one back puff. No wisps.
- **Mass.** A scalloped cloud around the hair centre, $62 \times 48\,u$ ($58 \times 46\,u$ in the small cut), with 9 lobes (7 in the small cut) from 222° to −42° (−36° small), quadratic control points at 1.18 times the radius, closed behind the face. It is filled with `--bertie-hair-shade`, so the valleys between tufts read as depth and a tuft swinging aside never shows the page through the hair. It stays inside the round ends: a larger mass fills the notches between tufts.
- **Merged outline.** The `g.hair-line` group draws the mass and every tuft in line colour with a stroke twice the outline width; the fills follow on top (mass, then back puffs, then the white tufts and wisps). The visible ring of line colour is therefore exactly one outline wide, around the union of all shapes, with no internal seams: a white puff meets a shaded one with no line, only the change of tone. Each tuft's outline copy takes the same spring transform as its fill, so the silhouette updates as the tufts swing.
- **Rejected geometry** [measured in the prototype]: draft 1's ring of sharp flame lobes (a crown of spikes; the face looked pasted on); draft 2's flame locks with pointed tips (too spiky, owner review); and, while drawing draft 3, ten round ends at an even 26° spacing (one solid cloud, an afro, with no tuft readable), club-shaped tufts over draft 2's large mass (a bumpy blob: the mass filled the notches), scallops 12 u long (crinkly at 160 px), two side clouds with no back puffs (a boxy wig, like earmuffs), an all-white crown (a cloud helmet, no depth), thin-stemmed wisps through the crown (a white stripe) and a narrow back crown (a parting at 96 px). From earlier drafts: straight, sharply pointed locks (a sunburst); a shade mass made of ten circles (the same look for 20 more elements); temple locks clipped to the face (a seam at 2x).

### 2.3 Drawing order (back to front)

1. Body group: neck, jumper, shirt V, bow tie.
2. Head group: hair group (outline silhouette, mass fill, back-puff fills, white tuft and wisp fills), ears, face, features group (blush, eyes with lids, brows, mouth, moustache, nose), orbit group.
3. Effects group (particles, bolt, sparks, z), outside the head so effects do not tilt with him.

The nose is drawn over the moustache and the moustache over the mouth: the classic layering that lets the mouth open "under" the moustache. Brows are drawn after the eyes, so a lowered brow overlaps the eye rather than hiding behind it.

### 2.4 Palette

Component tokens join `tokens.css`. They are fixed in both themes except `--bertie-shadow`.

| Token | Value | Use | Contrast note [measured] |
|---|---|---|---|
| `--bertie-line` | `#2A2420` | All outlines, eyes, lid edges | 15.3:1 on white; 1.1:1 on the dark surface, where fills carry the silhouette instead |
| `--bertie-skin` | `#F9D0AC` | Face, ears, lids | 12.8:1 on the dark canvas |
| `--bertie-skin-shade` | `#EFB089` | Nose, neck | |
| `--bertie-blush` | `#F2917A` | Cheeks, opacity 0.3 to 0.95 by state | |
| `--bertie-hair` | `#FFFFFF` | Front tufts and wisps | 18.4:1 on `#141414`, 16.7:1 on `#1E1E1E` |
| `--bertie-hair-shade` | `#E4E1EA` | Hair mass and the two back puffs (draft 3) | 14.3:1 on `#141414`; 1.3:1 on white, inside the outline |
| `--bertie-brow` | `#4A433E` | Brows | 6.8:1 on skin |
| `--bertie-tache` | `#F3F0EC` | Moustache | 1.3:1 on skin, so the outline (10.7:1) defines it |
| `--bertie-eye` | `#2A2420` | Eyes, closed and happy eye lines | 10.7:1 on skin |
| `--bertie-mouth` | `#6E2B26` | Mouth | 7.2:1 on skin |
| `--bertie-tongue` | `#E9806C` | Tongue | |
| `--bertie-jumper` | `#6F7D8E` | Jumper | 4.2:1 on white, 4.0:1 on the dark surface |
| `--bertie-shirt` | `#FFFFFF` | Shirt V | |
| `--bertie-tie` | `var(--pear-400)` | Bow tie | |
| `--bertie-orbit` | `var(--hint)` | Thinking electrons and orbit | 5.1:1 on white, 6.1:1 on the dark surface |
| `--bertie-zzz` | `var(--text-muted)` | Sleeping z | |
| `--bertie-shadow` | `rgba(0,0,0,0.10)` light, `rgba(0,0,0,0.45)` dark | Map-marker ground shadow | |

Effects borrow existing tokens: celebration squares in `--green-face`, `--green-frame`, `--pear-300`, `--pear-400`; streak bolt `--pear-400` with a `--pear-700` line; sparks `--pear-500`. No track colour appears on Bertie: track colours mean "this subject".

### 2.5 Line weights

All strokes are set in viewBox units from a target width in screen pixels, so the line looks the same at every size:

- Outline: $w_{\text{px}} = \operatorname{clamp}(\text{size}/70,\ 1.25,\ 2.6)$, then $w_u = w_{\text{px}} / s$ with $s = \text{size} / \text{viewBox width}$. At 220 px that is 2.6 px; at 96 px, 1.37 px; at 32 px, 1.25 px.
- Hair silhouette: drawn at $2w_u$, of which the outer half shows, so it matches the outline.
- Lid edges: $w_u$. Brows: $\max(6.4\,u,\ 1.8\,\text{px})$. Happy and closed eye lines: $\max(3.6\,u,\ 1.5\,\text{px})$.
- Joins and caps are round everywhere. Stroke alignment is centred (SVG default).

### 2.6 Levels of detail

| | Small cut (below 80 px) | Large cut (80 px and above) |
|---|---|---|
| viewBox | $(16, 10, 168, 168)$ | $(-8, -12, 216, 216)$ |
| Hair | 7 broad puffs (one a back puff), no wisps, 7-lobe mass, 22 u scallops | 10 tufts (two of them back puffs), 2 wisp puffs, 9-lobe mass, 16 u scallops |
| Body | Shoulder arc and shirt V | Bust with V-neck and bow tie |
| Face | Eyes ×1.2, brows lifted 5 u to clear them, no glints, no blush | Full |
| Line | 1.25 px | 1.25 to 2.6 px |
| Breathing | Off below 48 px | On |
| Elements | 74 | 92 |

Only the chosen cut is built at mount, from `size`. Both cuts share one state machine and one pose table; the small cut adds the eye boost and brow lift to every pose.

---

## 3. The SVG rig

```
svg.b-svg [data-state, data-eyes=open|happy|closed, data-lod=s|l]   aria-hidden, focusable=false
  defs: clipPath bz<n>-eye-l, bz<n>-eye-r, bz<n>-mouth              ids unique per instance
  g.figure              breathing bob                                Web Animations (infinite)
    g.body              shrug lift                                   CSS transform + transition
      g.neck            the visible neck the spring reveals
      jumper, shirt, g.tie (large cut)
    g.head              NECK SPRING: tilt, offset, stretch           transform attribute, spring integrator
      g.hair            hair-mass lag: rotation, vertical give       transform attribute, spring integrator
        g.puff          hair stands on end                           Web Animations
          g.hair-line   outline silhouette: mass + path.tuft-l[i]    (tuft-l[i] shares tuft[i]'s transform)
          path mass fill (hair shade)
          path.tuft[i]  HAIR TUFTS: 12 large, 7 small, each about its root   transform attribute, spring integrator
                        back puffs (f-hair-shade) first, then white tufts and wisps (f-hair); draft 3
      ears, face (with the hairline)
      g.features        three-quarter turn (away)                    CSS transform + transition
        g.blush-g       opacity by state (large cut)                 CSS opacity + transition
        g.eyes          gaze offset                                  CSS transform + transition
          g.eye-g[l|r]  EYES: scale (wide, small-cut boost)          CSS transform + transition
            g.eyeball   clipped to the eye; hidden for happy, closed
              eye, glint (large cut)
              g.lid-g   LIDS: closure and slant                      CSS transform + transition
                g.lid-b blink                                        Web Animations
                  lid fill, lid edge
            path.eye-happy, path.eye-closed                          shown by data-eyes
        g.brows         talking emphasis                             Web Animations
          g.brow-g[l|r] BROWS: lift, rotate (inner end up)           CSS transform + transition
        g.mouth-g       MOUTH: open amount and width; beats          CSS transform; Web Animations for beats
          mouth, tongue (clipped to the mouth)
        g.tache         MOUSTACHE: talking lift                      Web Animations
          g.tache-half[l|r]  corner lift (smile)                     CSS transform + transition
        nose
      g.orbits          thinking electrons and ring                  Web Animations
  g.fx                  particles, bolt, sparks, z                   Web Animations
```

The brief's named parts map one to one: head `g.head`; hair tufts `path.tuft[i]` with their outline copies; brows `g.brow-g`; eyes `g.eye-g`; lids `g.lid-g` and `g.lid-b`; moustache `g.tache`; mouth `g.mouth-g`; neck spring the `g.head` transform about the pivot, with `g.neck` as the part it reveals; body `g.body`.

Transform conventions:

- **One driver per element.** An element takes either a `transform` attribute (written by the spring integrator) or an inline CSS transform (pose transitions and Web Animations), never both, because CSS overrides the attribute. Where two drivers are needed, the rig nests two groups (`g.lid-g` for the pose, `g.lid-b` for blinks).
- **Explicit pivots.** CSS transforms are written as `translate(cx, cy) <op> translate(-cx, -cy)` in user units, with the SVG defaults `transform-box: view-box` and `transform-origin: 0 0`. This avoids `transform-box: fill-box`, whose box changes as shapes scale.
- **Pivots** [our choice]: head $(100, 150)$; hair mass $(100, 110)$; tufts at their roots; brows $(81, 86)$ and $(119, 86)$; eyes and lids at the eye centres; moustache $(100, 116)$; mouth $(100, 134)$.
- **Unique ids.** Clip paths are the only ids, prefixed `bz<n>-` from a module counter, so any number of instances share a page [measured: ids unique with 16 instances mounted on one page].

---

## 4. Motion system

### 4.1 Three drivers

| Driver | Moves | Why this driver |
|---|---|---|
| Spring integrator (`requestAnimationFrame`) | Head tilt and offset (the neck spring), hair-mass lag, every tuft and wisp | Must respond to any sequence of impulses and retargets without a jump, and couple the hair to the head's acceleration. Keyframes cannot |
| CSS transitions on inline transforms | Brows, eyes, lids, gaze, moustache corners, mouth, features turn, body, blush | A pose change is a jump to new values; the browser interpolates from wherever the channel currently is, so interrupted poses blend |
| Web Animations | Breathing, blinks, talking beats, hair puff, orbit, z, particles, bolt, sparks | Fixed, timed shapes; cancellable as a set when the state changes |

### 4.2 Springs

Each spring is a unit mass: $\ddot{x} = -k\,(x - x^{*}) - c\,\dot{x} + \text{drive}$, with damping ratio $\zeta = c / (2\sqrt{k})$.

| Spring | $k$ | $c$ | $\zeta$ | Units, clamp |
|---|---|---|---|---|
| Head tilt | 150 | 7.5 | 0.31 | degrees, none |
| Head vertical | 260 | 15 | 0.47 | u, none |
| Head horizontal | 220 | 15 | 0.51 | u, none |
| Hair-mass rotation | 200 | 9 | 0.32 | degrees, ±9 |
| Hair-mass vertical | 320 | 12 | 0.34 | u, ±6 |
| Tuft $i$ | $240\,k_i$, $k_i \in [0.85, 1.1]$ | 8.5 | 0.26 to 0.30 | degrees, ±16 |
| Wisp $i$ | $240\,k_i$, $k_i \in \{0.6, 0.65\}$ | 8.5 | 0.34 to 0.35 | degrees, ±30 |

- **Coupling.** Hair rotation is driven by $-0.55\,\ddot{\theta}_{\text{head}}$ and hair vertical by $-0.35\,\ddot{y}_{\text{head}}$. Tuft $i$ is driven by $-0.9\,\ddot{\theta}_{\text{head}} + 0.05\,\sigma_i\,\ddot{y}_{\text{head}}$, where $\sigma_i$ is $+1$ on the left, $-1$ on the right and $0$ on top (the two back puffs). The hair therefore lags and overshoots the head: follow-through without any authored keyframe.
- **Impulses.** `kick(va, vy, vx)` adds velocity to the head and transfers part of it: $\dot{\theta}_{\text{hair}} \mathrel{-}= 0.35\,v_a$, $\dot{y}_{\text{hair}} \mathrel{-}= 0.18\,v_y$, and to each tuft $-0.7\,k_i\,v_a + 0.28\,\sigma_i\,v_y$. Stiffness multipliers differ so tufts never move in lockstep; the wisps, softest, swing last and longest.
- **Integration.** Semi-implicit Euler at 240 Hz substeps; frame time clamped to 34 ms so a dropped frame cannot explode the system.
- **Sleep.** When every displacement and velocity is below a small threshold, the loop snaps to the targets and stops requesting frames. A still Bertie costs no frames [measured: `raf` is 0 within 3.5 s of a flick].
- **Squash and stretch.** The head stretches with vertical speed: $s = \operatorname{clamp}(-0.0005\,\dot{y}, -0.05, 0.05)$, scale $(1 - 0.6s,\ 1 + s)$ about the pivot.
- **Settling** [computed from the constants]: the tilt spring has natural frequency $\omega = \sqrt{150} \approx 12.2$ rad/s and damped period $2\pi / (\omega\sqrt{1-\zeta^2}) \approx 0.54$ s, so a 6° step overshoots by about 2.1° and comes to rest in about 1.5 s after two visible wobbles. The celebration hop (an impulse of 520 u/s on the vertical spring, $\zeta = 0.47$) lifts the head about 18 u off the neck at its peak.

### 4.3 Pose transitions

| Channel | Duration | Easing token |
|---|---|---|
| Brows, moustache corners | 260 ms | `--spring-bounce` |
| Eye scale | 200 ms | `--spring-bounce` |
| Lids | 180 ms | `--ease-standard` |
| Gaze | 140 ms | `--ease-standard` |
| Mouth | 180 ms | `--ease-standard` |
| Features turn (away) | 360 ms | `--ease-morph` |
| Body (shrug) | 220 ms | `--spring-bounce` |
| Blush | 300 ms | `--ease-standard` |
| Eye mode (open, happy, closed) | instant swap | none; a cartoon eye change is a cut |

Lids use `--ease-standard`, not a spring: an overshooting lid would flash the top of the eye.

### 4.4 Life

- **Breathing.** `g.figure` rises 1.6 u and returns over 3,200 ms, ease-in-out, looped. Sleeping: 3 u over 4,400 ms. Map marker (`float`): 6 u over 2,000 ms. Off below 48 px, off in `away`, off when offscreen, off under reduced motion.
- **Blinks.** Each lid drops from its pose closure to shut and back in 150 ms (ease-in-out, shut at 45%), every 2.5 to 6 s at random, 20% of them double. While thinking, every 4.5 to 8 s. No blinks in `sleeping` or `away` (eyes already closed).
- **Fidgets (idle only).** Every 5 to 10 s: a glance to one side for 0.9 to 1.5 s (45%), a small head sway impulse of up to 30°/s (30%), or a brow lift of 3.5 u over 520 ms (25%). A glance never fires while the app has set a gaze target.
- **Quiet.** `quiet(true)` pauses breathing, blinks and fidgets while the learner drags on a canvas ("motion follows only the learner's input", design research section 1). The app calls it on pointer-down inside any interactive widget and releases it on pointer-up.

### 4.5 Interruption rules

- `setState` cancels the previous state's timers and Web Animations and clears the effects group. Springs are never reset: they retarget from where they are, so a state change mid-wobble blends.
- A one-shot returns to the held state that was current when it started, or to `opts.then`.
- `celebrate`, `streak`, `sleeping` and `away` close any open speech bubble: their effects need the space above him, and he is not speaking.
- A finished reply (`say` with `end()`) returns to the held state before it, except that `thinking`, `listening` and `talking` return to `idle`: he never goes back to waiting after he has answered.
- Tapping Bertie (when `interactive`) adds an impulse proportional to the tap's horizontal offset from his centre and a blink. It changes no state.

---

## 5. States

### 5.1 State table

All poses are offsets from the neutral pose. "Brows" gives lift (u, negative is up) and inner-end rotation (degrees, positive raises the inner end). "Lids" gives closure (0 open, 1 shut) and slant (degrees, positive lowers the outer ends). "Smile" is the moustache corner lift in degrees. "Mouth" is the vertical opening, where 0.25 is the resting smile.

| State | Kind | Trigger in the app | Pose | Motion (full) | Reduced motion | Ends |
|---|---|---|---|---|---|---|
| `idle` | held | Default; Continue after a verdict; a reply finishes | neutral; lids 0.1, 6°; smile 3°; mouth 0.25 | breathing, blinks, fidgets | blinks only | on next state |
| `listening` | held | Learner types in the tutor composer | tilt 2° plus up to 4° towards the target; brows −2, +2°; lids 0.04; eyes on the composer (fallback glance down-right) | blinks; gaze follows `lookAt` | static pose, blinks | on submit (to `thinking`) |
| `thinking` | held | A tutor call starts, until the first text (`AI-TUTOR.md` 7.4) | tilt −5°; one brow up (−7 u), the other level and knitted; that eye's lid at 0.34 (a sceptical squint); eyes up-right; moustache pursed to one side; mouth 0.16, narrow | three electrons orbit his head once per 1.2 s, 400 ms apart, on a dashed ring tilted −12°; slow blinks | three static electrons on the ring | first text delta (to `talking`) |
| `talking` | held | Reply text streaming; `say()` | brows −1, +1°; smile 5°; mouth 0.3 | each text delta: mouth opens to 0.6 to 0.95 and closes in 170 ms, moustache lifts 2 u; every 4th beat a brow lift, every 5th a micro-nod; at most 6 beats a second | no beats | `end()`, to the previous held state or `idle` |
| `correct` | held | After Check, answer right | head up 2 u; brows −5, +3°; lids 0.16, 3° (content); smile 11°; mouth 0.55; blush 0.8 | happy squint for 650 ms; nod from two downward impulses (0 and 260 ms) | pose only, no squint, no nod | Continue (to `idle`) |
| `notyet` | held | After Check, answer not yet right | tilt 6°; brows −4, +10° (inner ends up: sympathy); lids 0.2, 14°; smile 6°; mouth 0.24, narrower; eyes slightly down | tilt lands on the spring, encouraging nod at 480 ms | pose only | Try again (to `idle`) |
| `curious` | held | Tutor reply with `face: "curious"`; Explore screens | tilt −7°; one brow −9 u, the other +1 u and knitted, its lid at 0.26; eyes up-right | a sideways flick on entry | pose only | on next state |
| `sleeping` | held | Rest day on Today; streak freeze in use | tilt 9°, head down 4 u; eyes closed (a ∪ line); mouth a small "o" (0.4, narrow); blush 0.6 | slow breath (4.4 s); three z rise and fade over 3 s, 1 s apart | three static z | on next state |
| `away` | held | Timed exam running; homework item open | tilt −4°; features turned 8 u aside (three-quarter turn); eyes closed | none; no breathing | same | exam submitted (to `idle`) |
| `point` | held | Tutor act line highlights an element (`highlight`, `AI-TUTOR.md` 5.3) | tilt up to 9° and offset 4 u towards the target; brows −5 and −7 u; lids open; eyes on the target | two nudges towards the target, 420 ms apart | pose only | on next state |
| `celebrate` | one-shot, 1.9 s | Lesson complete; exam passed | happy eyes (∩); big open smile with tongue (mouth 1.0); blush 0.95 | sink 6 u (150 ms anticipation), hop (impulse −520 u/s with a random sideways spin), hair puff, 12 squares burst from a ring outside his face (700 ms), second hop at 760 ms, sway at 1,150 ms | static ring of 12 squares, fading out by 1.15 s | returns to held state |
| `streak` | one-shot, 1.7 s | Streak extended (design research 6.2) | eyes wide (×1.12) and up; lids open; brows −9 u; smile 10°; mouth 0.7 | pear bolt pops in above his head (spring overshoot to 1.18), hangs while he looks up, strikes down into his hair at 780 ms; hair puffs, tufts flare and six pear sparks fly; happy squint; nods at 1,150 and 1,400 ms | bolt shown still, fading out by 1.15 s | returns to held state |
| `surprised` | one-shot, 0.9 s | A counter-intuitive reveal (a Trap screen's reveal, Monty Hall) | eyes ×1.3; lids open; brows −12 u; mouth an "o" (0.9, narrow) | jolt up (−330 u/s), hair puff and tuft flare | pose only, held 0.9 s | returns to held state |
| `shrug` | one-shot, 0.8 s | Tutor errors (`AI-TUTOR.md` 7.5 rows marked shrug) | shoulders up 7 u; tilt −4°; uneven brows and lids (0.28 and 0.08); moustache crooked | shoulders drop back at 380 ms; head sway | pose only | returns to held state |

### 5.2 Aliases

`speaking` → `talking`; `pleased` → `correct`; `concerned` and `encouraging` → `notyet`; `rest` → `sleeping`; `pointing` → `point`; `complete` → `celebrate`. The tutor's act-line `face` values (`pleased`, `curious`, `concerned`) therefore map directly. An unknown name throws `RangeError`: a typo is a programming error, caught in tests, never a silent idle.

### 5.3 Who drives the states

| Source | Calls |
|---|---|
| Lesson player (state machine, design research 5.4) | `correct` or `notyet` on grading; `idle` on Continue or Try again; `surprised` on a Trap reveal; `celebrate` on lesson complete; `quiet(true/false)` around canvas drags |
| `TutorService` (`AI-TUTOR.md` section 6) | `listening` on composer input; `thinking` on call start; `talking` plus `pulse()` per delta; `idle` on end; `shrug` on error codes; `point` with the highlighted element; the reply's `face` |
| Exam and homework screens | `away` while locked; `idle` after submission |
| Streak service | `streak` at the moment the count changes (numbers move with the picture, design research 4.1 principle 2) |
| Today screen | `sleeping` on a rest day or an active freeze |

One rule protects the boundary principle: during a problem only `idle`, `listening`, `thinking`, `talking`, `point` and `curious` may play. Energetic states (`celebrate`, `streak`, `surprised`) belong to boundaries.

---

## 6. Reduced motion

- **Detection.** `data-motion="reduced"` on `<html>` (the app's Motion setting) wins; `data-motion="full"` forces full motion; otherwise `prefers-reduced-motion: reduce` decides. Instances listen for changes to either and rebuild their current state.
- **What stops.** The spring integrator (every target is applied at once), breathing, fidgets, talking beats, nods, hops, the puff, the orbit's travel, rising z, flying particles and sparks.
- **What remains.** Pose changes (applied at once: `components.css` already forces transitions to 1 ms), eye modes, lid poses, blinks (a lid drop with no travel of the figure; `AI-TUTOR.md` 7.2 keeps them), and static versions of effects: three still electrons, three still z, a still ring of squares, a still bolt. Static effects fade out by opacity only.
- **Durations.** One-shots are capped at 1.2 s, so the return to the held state is not delayed for a learner who sees no motion.
- **Tap.** A tap blinks him instead of flicking.

---

## 7. Where he appears

| Place | Size | Cut | States used | Notes |
|---|---|---|---|---|
| Verdict bubble, bottom-left of the lesson card | 32 | small | `correct`, `notyet`, `talking` | Bubble tail points at him (`AI-TUTOR.md` 7.1) |
| Exam top bar | 32 | small | `away` | With the text "Bertie is out of the room until you submit" |
| Lesson dock; mobile hint-slot button; chat drawer header | 40 | small | `idle`, `listening`, `thinking`, `talking`, `point` | Inside a 48 to 52 px button labelled "Ask Bertie, the tutor" |
| Notebook pins, settings row | 32 | small | `idle` | No breathing below 48 px; blinks only |
| Course map, over the current node | 64 | small, `float` | `idle`, `talking` | 2 s hover, ground shadow; tap opens a bubble with the next lesson's title |
| Today, rest day | 96 | large | `sleeping` | "Rest day. Your streak is safe." beside him |
| Streak sheet | 120 | large | `streak` | The count changes at the bolt's strike (780 ms) |
| Lesson complete; exam result | 160 | large | `celebrate`, then `correct` | Skippable with the rest of the celebration (tap anywhere) |
| Onboarding host | 160 | large | `talking` with `say()`, `idle`, `curious` | Questions in his bubble (Brilliant's onboarding pattern, design research 3) |
| First-run tutor card (`AI-TUTOR.md` 7.9) | 96 | large | `idle`, `talking` | |

- **At most three animated instances on one screen.** Others mount in `idle` with `quiet(true)`. In practice no screen needs more than two.
- **"Show Bertie" off** (`AI-TUTOR.md` 7.7): the app's logo mark fills his slots and none of this code mounts.

---

## 8. Accessibility

- **Decorative by default.** The SVG carries `aria-hidden="true"` and `focusable="false"`. Every state that matters has text next to it: the verdict line, "Thinking", the exam notice, the rest-day line, error copy (`AI-TUTOR.md` 7.5 and 7.8). A screen-reader user loses nothing.
- **If ever informative.** `mount(el, { label })` switches to `role="img"` with that label. Copy pattern: "Bertie, the tutor, " plus a state phrase: "waiting", "listening", "thinking", "talking", "pleased", "encouraging you", "curious", "asleep", "looking away", "pointing", "celebrating", "cheering your streak", "surprised", "shrugging". Never "Einstein" (decision 12). No screen uses this today.
- **Buttons.** A control that contains Bertie names itself ("Ask Bertie, the tutor"); Bertie inside it stays hidden.
- **Speech bubble.** Plain text only. No live region by default: the app announces the complete reply once through its shared polite region ("Bertie says: ..."), never partial text (`AI-TUTOR.md` 7.8). `say(..., { announce: true })` adds `aria-live="polite"` for a standalone page such as onboarding.
- **Flashing.** Nothing flashes more than once in any second; the sparks are a single burst, inside WCAG 2.3.1's three-flash limit.
- **Contrast.** Bertie is decorative, so WCAG 1.4.11 does not bind him, but the silhouette meets 3:1 on both canvases anyway: the outline on light (15.3:1), white hair on dark (16.7:1 or more) [measured].
- **Tap to flick.** Pointer-only and not focusable: it carries no function or information, so keyboard users lose nothing (WCAG 2.1.1 covers functionality).
- **Reduced motion.** Section 6. The app's Motion setting overrides the system preference in both directions.

---

## 9. Performance and size budget

| Measure | Budget | Measured [measured, 7 October 2026, draft 3] |
|---|---|---|
| `bertie.js` plus `bertie.css`, minified and gzipped | 12,000 bytes | 11,067 bytes together (JS alone 9,905, CSS alone 1,305); esbuild 0.24, `gzip -9`. Draft 2 was 10,615; the rounded-tuft code adds about 460 bytes |
| Minified | none | 31,976 bytes (JS 27,763, CSS 4,213) |
| Source | none | 49,831 bytes (JS 44,405, CSS 5,426) |
| SVG elements per instance | 100 | 92 large cut; 74 small cut |
| External requests | 0 | 0: no images, fonts or network |
| Frames when still | 0 | 0: the integrator sleeps at rest |

- **Offscreen.** An `IntersectionObserver` pauses breathing, blinks and fidgets for instances outside the viewport.
- **Small instances** (below 48 px) do not breathe: a 1 px bob is invisible at that size but still repaints.
- **Paint cost.** SVG transforms repaint the SVG rather than compositing, and each tuft writes two transforms per frame while the hair moves. The three-instance rule (section 7) bounds the cost. Frame rate on a phone has not been measured [unverified]; section 13 item 3 sets the Phase 2 check.

---

## 10. JavaScript API

The module exports one function, `mount`. The brief's five calls (`mount`, `setState`, `lookAt`, `say`, `destroy`) are all present; `pulse`, `quiet`, `flick` and `closeBubble` are additions the tutor and lesson player need.

```ts
type HeldState = 'idle' | 'listening' | 'thinking' | 'talking' | 'correct' | 'notyet'
               | 'curious' | 'sleeping' | 'away' | 'point';
type OneShot   = 'celebrate' | 'streak' | 'surprised' | 'shrug';
type Alias     = 'speaking' | 'pleased' | 'concerned' | 'encouraging' | 'rest' | 'pointing' | 'complete';

interface MountOptions {
  size?: number;          // CSS px, default 160; below 80 picks the small cut
  interactive?: boolean;  // tap to flick; default false
  label?: string;         // makes him an informative image (role="img"); default decorative
  float?: boolean;        // course-map hover in place of breathing
}

interface SayOptions {
  place?: 'auto' | 'right' | 'top';   // auto: right if 220 px fit inside the bounds, else top
  tone?: 'plain' | 'correct' | 'notyet';
  stream?: boolean;       // true: text arrives through append(); false: he talks for 0.7 to 4 s by word count
  announce?: boolean;     // aria-live="polite" on the bubble; default false
  within?: Element;       // bounds for placement (16 px gutter); default the viewport
}

interface BubbleHandle { append(delta: string): void; end(): void; close(): void; }

interface Bertie {
  readonly state: HeldState | OneShot;
  readonly root: HTMLElement;           // dispatches 'bertie:state' (detail: { state }), bubbling
  setState(name: HeldState | OneShot | Alias, opts?: { at?: Element | { x: number; y: number } | null; then?: HeldState }): Promise<void>;
  lookAt(x: number, y: number): void;   // client coordinates
  lookAt(target: Element | null): void; // null clears
  say(text: string, opts?: SayOptions): BubbleHandle;
  closeBubble(): void;
  pulse(): void;                        // one talking beat; rate-limited to 1 per 160 ms
  quiet(on?: boolean): void;            // hold still during canvas manipulation
  flick(e?: { clientX: number }): void; // the tap impulse, callable by the app
  destroy(): void;                      // cancels timers, animations, frames, observers; removes the DOM
}

export function mount(el: Element, opts?: MountOptions): Bertie;
```

Contracts:

- `setState` resolves at once for a held state and when a one-shot has finished and returned. It throws `RangeError` for an unknown name.
- `lookAt` re-aims at once; in `point` and `listening` it also retargets the head tilt. A target that is an `Element` is re-measured on each call, so callers re-call `lookAt` after layout changes.
- `say` replaces any open bubble, switches to `talking`, and sets text through `textContent`. The bubble stays open after `end()` so the learner can read it, until `close()`, the next `say`, or a state that closes it (section 4.5). Untrusted text (a model reply) is therefore safe here; Markdown and KaTeX belong to the tutor's own reply component.
- `destroy` is idempotent in effect: after it, the instance holds no timers, animation frames, observers or listeners.

Example, the tutor lifecycle. The chat drawer renders the reply itself (Markdown, KaTeX, sentence gating per `AI-TUTOR.md` 7.3); Bertie only acts it out:

```js
const bertie = mount(dockEl, { size: 40 });
bertie.setState('thinking');                  // call starts
backend.ask(request, {
  onText: delta => {                          // a sentence passed the gates and was shown
    if (bertie.state !== 'talking') bertie.setState('talking');
    bertie.pulse();                           // one beat; rate-limited inside
  },
  onDone: () => bertie.setState('idle'),
  onError: () => bertie.setState('shrug'),    // one-shot, then back to the held state
});
```

Bubbles that Bertie owns (onboarding, the map marker, the streak sheet) use `say()`:

```js
const hostBertie = mount(onboardingEl, { size: 160 });
hostBertie.say('What brings you here?', { within: cardEl, announce: true });
```

---

## 11. Why SVG and Web Animations, not Rive

| Criterion | Rive | Lottie (`lottie-web`) | Canvas 2D | SVG + springs + Web Animations (chosen) |
|---|---|---|---|---|
| Runs in the Artifact host | Not as shipped. The web runtime fetches its WebAssembly binary from a CDN by default [recalled, unverified], and the Artifact blocks every fetch to another host [sourced, brief]. Self-hosting is now plausible: the Artifact probe ran WebAssembly in the page and in a worker and fetched published `.wasm` files on the owner's iPhone [sourced, `spikes/README.md`]. A self-hosted Rive build has not been tried [unverified]. The `.riv` asset is not a served file type [sourced], so it would ship base64-encoded inside a `.js` or `.json` file | Probably: cdnjs is an allowed script host and `.json` is served [sourced]; that cdnjs carries `lottie-web` is [recalled, unverified] | Yes | Yes: own files only, no WebAssembly |
| Runtime weight | Hundreds of KB including WebAssembly [recalled, unverified] | About 250 KB minified [recalled, unverified] | None | 11,067 bytes gzipped, everything included [measured] |
| Physics, gaze, per-delta speech | State machines and inputs, yes; live springs only through its own tooling | No: plays authored timelines | Yes, all hand-written, including hit-testing and device-pixel handling | Yes |
| Theme tokens | Through data binding or a second file | Recolouring at runtime | Read tokens in JS | CSS variables directly |
| Two levels of detail | Two artboards to keep in step | Two files | Code | One rig, two tables (section 2.6) |
| Authoring and review | Proprietary editor; binary file; no meaningful diff | After Effects plus Bodymovin; large JSON diffs | Code | Code and data in the repo; geometry is generated from numbers (section 2.2), so a change is a reviewable diff |
| Reduced motion | Separate state or file | Separate file or stop | Hand-written | One switch in the controller (section 6) |

Brilliant builds its motivational animation in Rive state machines [sourced, design research 4.1]. We keep the idea (explicit state graphs, inputs fired by the app) and implement it in code. The brief's reason, that the Artifact CSP blocks Rive's runtime fetches, holds for Rive as shipped. The spike's WebAssembly result removes the hard block for a self-hosted build, so the decision now rests on the other rows: an 11 KB component with live springs, gaze, per-delta speech and CSS tokens, reviewable as text, against a runtime in the hundreds of KB with a binary asset and an editor nobody on the project uses. Revisit only if an animator who works in Rive joins (section 13).

---

## 12. Build layout and tests

### 12.1 Files

| File | Contents | Origin in the prototype |
|---|---|---|
| `src/ui/bertie/geometry.ts` | Pure functions and tables: `tuftPath`, `massPath`, `RING`, `CHORD`, `PLAIN`, `SCALLOP`, `STIFF`, `TUFTS`, `MASS`, `FACE_D`, moustache and mouth paths, key points | the constants block |
| `src/ui/bertie/poses.ts` | `POSES`, `HELD`, `ONE_SHOT`, `ALIAS`, `LIFE`, `CLOSES_BUBBLE` | verbatim |
| `src/engine/motion/spring.ts` | Pure integrator shared with widgets (`ARCHITECTURE.md` 5.11): `step(state, targets, tufts, dt) -> state`, `atRest(state)` | `_tick` body, without DOM |
| `src/ui/bertie/markup.ts` | `svgMarkup(lod, id)` and the `DOMParser` call (decision 19) | `svgMarkup` |
| `src/ui/bertie/bertie.ts` and `Bertie.tsx` | `mount` and the controller; `Bertie.tsx` is the Preact wrapper that mounts the rig imperatively (`ARCHITECTURE.md` decision 28) | the rest of the component script |
| `src/ui/bertie/bertie.css` | Rig and bubble styles | the `bertie.css` block |
| `src/styles/tokens.css` | `--bertie-*` tokens (section 2.4); amended pear comment | |

Splitting geometry, poses and the integrator out of the DOM code makes each one unit-testable without a browser.

### 12.2 Tests

| Test | Check | Tool |
|---|---|---|
| Spring | Each spring settles within 2.5 s from a 15° step and from a 500 u/s impulse; no NaN at $dt$ = 1 ms or 34 ms; `atRest` true at the end | Vitest |
| Geometry | Paths are closed and finite; every tuft root lies inside the mass; every scallop arc bulges outwards (its sweep flag matches the outline's winding); small-cut shapes lie inside the small viewBox plus 4 u; ring angles symmetric about 90° | Vitest |
| State machine | Every alias resolves; unknown throws `RangeError`; one-shots return to the prior held state or `then`; a reply after `thinking` ends in `idle` | Vitest with a DOM shim |
| Speech safety | `say('<img src=x onerror=...>')` renders the literal text, creates no element and runs no script | Playwright [passed, draft 2] |
| Rate limit | 20 `pulse()` calls in one tick produce 1 beat | Playwright [passed, draft 2] |
| Sleep | Frames requested during a flick; none 3.5 s after it; none at all under reduced motion | Playwright [passed, draft 2] |
| Ids | Clip-path ids unique with several instances mounted | Playwright [passed, draft 2] |
| Clean-up | `destroy()` leaves the host element empty | Playwright [passed, draft 2] |
| Visual regression | Every state at 32, 96 and 220 px, light and dark, against baselines (one-shots captured at fixed points of a paused animation clock) | Playwright screenshots |
| Accessibility | SVG `aria-hidden`; no focusable descendants; axe clean on the demo page | axe-core |
| Size | `bertie.js` plus `bertie.css`, minified and gzipped, at most 12,000 bytes; at most 100 elements per instance | CI script |

### 12.3 Prototype verification (done, draft 2)

- Screenshot harness on `prototype/bertie.html`, widths 390 and 1,280, light and dark, with actions for thinking, a streamed reply, not yet, point, celebrate, streak, sleeping, a spoken hint, reduced motion, surprised and the theme toggle: "no errors", no horizontal overflow [measured]. A second pass at 390 px captured the bubble, thinking and the reduced-motion celebration at the top of the page.
- Every state inspected at 1x as a contact sheet in both themes, and the idle large cut at 2x and 3x [measured].
- One-shots inspected as timed filmstrips at 1x: `celebrate`, `streak`, `surprised` and `correct` in light [measured]. The hop shows the neck stretch; the locks lag and overshoot the head; the wisps settle last.
- At 32 px, 1x, in both themes, he reads as a white-haired professor with a moustache; the dome, brows, eyes and moustache stay separate [measured].
- Behaviour checks in Chromium (section 12.2 rows marked passed) and the size measurement in section 9 [measured].

### 12.4 Prototype verification (done, draft 3, 7 October 2026)

- Screenshot harness on `prototype/bertie.html`, widths 390 and 1,280, light and dark, with actions for thinking, a streamed reply, not yet, point, celebrate, streak, sleeping, a spoken hint, reduced motion, surprised, the theme toggle and the sizes row: "no errors", no horizontal overflow [measured]. A second pass at 390 px, scrolled to the stage, captured thinking, not yet, curious, the hint bubble, streak, away and shrug in both themes: "no errors" [measured].
- The hair was chosen over eleven rounds (three single edits, then eight sets of variants), each rendered at 2x on the 220 px stage and at 1x across the size row (section 2.2 lists the rejected ones) [measured].
- Every state inspected in both themes; the idle large cut at 2x; mid-swing frames of `celebrate` (light) and `streak` (dark) at 2x show no seams where puffs part [measured].
- One-shots inspected as timed filmstrips at 1x: `celebrate`, `streak` and `surprised` in light [measured]. The puffs lag and overshoot the head, flare on the hop and the bolt's strike, and settle; the wisps swing widest. Sparks and the square burst start outside the hair.
- At 32 px, 1x, in both themes (size row, verdict chips, exam bar), he reads as a white-haired professor with a moustache: a skin dome inside a round, scalloped white halo [measured].
- Geometry [measured, `getBBox`]: 92 elements large, 74 small (unchanged); the small cut's hair lies inside its viewBox; clip-path ids unique with 14 instances on the page. Size in section 9.

---

## 13. Open questions

1. **Name and likeness for a public launch.** The art is a generic caricature and the copy never names a real person (decision 12). If the app is ever published commercially, the owner should take advice on whether an Einstein-style character needs clearance [recalled, unverified: the name and likeness are licensed commercially].
2. **Rive later?** Only if an animator who works in Rive joins, and only after a self-hosted runtime is shown to load in the Artifact. The API in section 10 would stay; only the renderer would change.
3. **Mid-range phone check.** Confirm 60 fps for a 160 px celebration on a mid-range Android phone and the owner's iPhone in Phase 2. If it drops, first stop the outline copies following the tufts during one-shots (the fills still swing; the silhouette lags by one shape), then cut the particles to 8.
4. **Sound.** Bertie makes no sound of his own; the app's event sounds (design research 4) play alongside him. Revisit only if testers ask for a voice.
5. **Wisps at 96 px.** At 1x the two wisp puffs read cleanly at 96 px, as small flyaways below the side puffs [measured, draft 3]. If the rest-day card looks busy in Phase 2 review, drop the wisps below 120 px rather than adding a third cut.
6. **Owner sign-off on the hair.** At the 7 October 2026 review the owner confirmed draft 2 as drawn except the hair, which draft 3 redraws. The owner should confirm the draft 3 hair before Phase 2 builds the baselines for visual regression; the face needs no further sign-off.
