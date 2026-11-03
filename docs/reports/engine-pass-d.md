# Engine pass D: the `trade` widget (E12) and carried values

Items 459 and 460 of `docs/ENGINE-BACKLOG.md`. Built on engine pass B (456 to 458).

## Items

- **459 (inbox E12): `trade` widget.** A market-making game over the `orderbook` canvas. The learner sets bid, ask and size each turn; a seeded counterparty trades at the quoted price; cards arrive on a schedule; a position limit applies; a ledger shows position, cash, mark-to-market and realised P&L; the hidden value settles the position after the last turn. Grade: final P&L against a benchmark or band, then rule breaks.
- **460 (inbox "running ledger"): carried values.** `carry: "name"` on a widget stores the learner's value at check or reveal; a later screen reads `{{carry.name}}` in any string of its spec. The trade widget carries its whole ledger.
- Inbox bullets integrated: E12 and the running ledger bullet (both removed from `docs/BACKLOG-INBOX.md`). The mm-games bullets in the inbox (`table` wrong ids, `sliders` boolean checks, number-line interval drag, log tick separators) are not answered by E12 and stay. The game-theory `play` bullet is related but separate and stays.

## Files

- New: `app/js/engine/widgets/trade.js` (the pure game, exported to Node as `module.exports`, plus the widget); `app/content/exams/mock-trade-sample.json` (sample mock exam, on no course map; manifest picks it up).
- Edited: `app/index.html` (script tag), `app/css/widgets.css` (`.wd-trade*`, tokens only, 480 px breakpoint), `app/js/engine/player.js` (`carryResolve`, `carryReset`, `storeCarry`; `Z.player.carryReset`), `app/tools/validate.mjs` (widget kind, `case 'trade'`, carry checks), `docs/AUTHORING.md` (section 3 `trade` and "Carried values", section 7 rule 4), `app/js/engine/canvas/README-B.md` (orderbook note), `docs/ENGINE-BACKLOG.md` (459, 460 and the pass D status block), `docs/BACKLOG-INBOX.md`.
- No content file was edited. Scratch work is in `<scratchpad>/engine-pass-d/`.

## How the game works

- Deterministic: the counterparty's three draws for turn `t` come from `seed` and `t` only (mulberry32), so the same quotes always meet the same counterparty and the learner can retry a miss (Try again restarts at turn 1).
- `noise`: chance `rate` (0.6), random side, size 1 to `maxSize`, optional `reach` from the mark. `informed`: knows the value; lifts the ask if `value - ask > edge`, hits the bid if `bid - value > edge`, for the full quoted size. `scripted`: `trades: [{ act: "hit" | "lift" | "none", size, price }]` per turn, `price` a limit. A list of counterparties is chosen by each entry's `turns: [first, last]`.
- Rule breaks (one per turn and kind): `limit` (size above the room either side; the quote is cut back to the room), `crossed` (bid at or above ask; rejected, nobody trades), `spread` (outside `spread.min` and `spread.max`; still goes out). The learner sees a warning under the inputs before sending.
- Ledger: average-cost realised P&L; mark-to-market is cash plus position at the mark (opening `fair`, moved by cards' `fair`); final P&L is cash plus position at `value`. Realised includes the settlement.
- Grade keys: `low`, `high` (band only), `limit`, `crossed`, `spread`. Breaks beyond `maxBreaks` fail first, then P&L.
- `ZQ.test.answerCorrect()`, Show solution and the exam hook replay the authored `strategy`; the validator plays the same strategy through the same module and errors if it does not meet the target with no breaks, so the playthrough cannot meet an unbeatable game.

## Worked example (also in AUTHORING section 3)

```json
{ "kind": "trade", "seed": 6, "turns": 8, "fair": 100, "value": 103, "tick": 0.5, "range": [94, 108], "currency": "£",
  "size": { "min": 1, "max": 3, "start": 1 }, "limit": 4, "spread": { "min": 1, "max": 4 }, "quote": { "bid": 98, "ask": 102, "size": 1 },
  "counterparty": [ { "type": "noise", "rate": 0.8, "turns": [1, 4] }, { "type": "informed", "edge": 0.5, "turns": [5, 8] } ],
  "schedule": [ { "turn": 1, "text": "The share last traded at £100." },
                { "turn": 4, "text": "A report beats forecasts. Fair is now £101.50.", "fair": 101.5 },
                { "turn": 7, "text": "The value is revealed: £103.", "reveal": true } ],
  "benchmark": 8, "maxBreaks": 0,
  "strategy": [ { "bid": 99, "ask": 101, "size": 2 }, { "bid": 99, "ask": 101, "size": 2 }, { "bid": 99, "ask": 101, "size": 2 }, { "bid": 99, "ask": 101, "size": 2 },
                { "bid": 100.5, "ask": 103.5, "size": 1 }, { "bid": 100.5, "ask": 103.5, "size": 1 }, { "bid": 100.5, "ask": 103.5, "size": 1 }, { "bid": 100.5, "ask": 103.5, "size": 1 } ] }
```

Put it on a screen (or set or exam item) with `"canvas": { "kind": "orderbook", "params": { "bids": [[98.5, 300], [98, 500]], "asks": [[101.5, 200], [102, 400]], "depth": 3, "currency": "£", "dp": 1, "showMid": true } }`, a `feedback` with `correct`, `generic` and `byKey` lines for `low`, `limit`, `crossed` and `spread`, and an `explain`. To feed the result forward, add `"carry": "desk"` and write `{{carry.desk.pnl}}` on a later screen (a canvas state value, prose, or a numeric `answer`).

## Results

- Validator: 0 errors. Scratch cases (copy of the app in the scratchpad) all gave the intended line: missing or fractional seed, bad counterparty type or fields, scripted without trades or with a bad `act`, card turn out of range, card without text, both or neither of benchmark and band, missing or short strategy, strategy that misses the target, breaks a limit or crosses, limit 0, unknown field, bad range, `byKey.high` without a band, a non-orderbook canvas (warning), a trivial benchmark (warning); carry: a read with no store (error), a store then a read (clean), a bad carry name (error).
- Playthrough: `--exam mock-trade-sample` green with and without `--mobile`; `--routes-only` green. The full run in shards: see the final line of the hand-back.
- Browser checks (scratch Playwright): an exam page driven by real clicks, keyboard arrows and Enter (Enter sends and does not also press Check); a lesson mounted from an object: a failed run grades `low` with the line, Try again restarts at turn 1, a correct run grades ok, `carry` fills prose, a canvas `fair` as a number and a numeric `answer`, with the fallback shown for an unknown name. Screenshots, light and dark at 1280 and 390 px, mid-game and at results, inspected: no sideways page scroll, ledger two by two on the phone, results table wraps inside the box.

## Follow-ups

1. The real mm-games content can now replace its scripted drills with `trade` screens; that is a content pass. Level files were not touched.
2. `carry` is held in memory: reopening a lesson part-way loses it (the fallback or 0 shows). Persisting it with the lesson position is a small change if a lesson needs it.
3. Exam and homework items are all drawn at once, so they cannot read a carried value (a lesson or a set can). A lazily drawn item would lift that.
4. The game-theory `play` widget (rounds against a seeded mixed strategy) could reuse the pure game's draws and ledger; not built.
5. One size for both sides and one price tick; separate bid and ask sizes, a passive order that rests across turns and a two-sided counterparty that can trade both sides in a turn are not built.
6. No Why? replay of the learner's own run turn by turn (Show solution replays the authored strategy).
