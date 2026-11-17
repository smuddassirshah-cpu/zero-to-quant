# Engine pass 7 remainder, package 2 (validator rules and number scripts)

Base 74f4f090 on `claude/session-ah-engine-pass-1nzn58`. All rules are warnings; the validator ends at 0 errors on current content. Hits: `docs/reports/engine-pass-7r-pkg2-hits.md`. Tests: `app/tools/test-validate-pkg2.mjs` (36 cases, in `acceptance.yml`), `test-numbers-lib.py` extended; still green: `test-validate-pass8`, `-pass9`, `-shown-arithmetic`, `-problems`, `-near-miss`, `-wrong-fire`, `-harness`.

## Built
- **1029** `slip` expression on a `wrong[]` entry (also a table cell's); `[slip-expr]`; `numbers_lib.py` `check_slips` (one grammar in JS and Python).
- **1079** `[no-chain]`: no later part cites an earlier part, "Using $...$", or an earlier key (7 hits).
- **1081** `Level.slip(ref, path, wid, *routes)`: each route inside the slip band, outside the key band, bands apart, `byKey` line present.
- **1130** `[carry-band]` (128 hits: many bands narrower than the key's by design; the list may be too long, tighten if so).
- **1138** `[quotient-band]` (0 hits; the garch/numerics case is now in band).
- **1142** `[shown-arithmetic]` reads "x is $a \times b$" and `\Phi\big(a/b\big) = \Phi(x)` (2 hits).
- **1175** `[slip-in-key-band]` (2 hits). The literal case (0.3333 +-0.001 at 2 places) was already `[wrong-band]`.

## Seams
`validate.mjs` never rejected unknown fields on a `code` widget, so package 1 needed nothing for 1028 and 1037. For 951 I allowed the `byKey` keys `percent-sign` and `decimal` on a numeric widget. CI lines added for `test-fresh-check-pkg3` and `test-grade-code` (the latter two files are not in this worktree).

## Backlog
Triage applied in one block: 8 `status: open` lines remain, the [Should] items 1154, 1158, 1182, 1190, 1203, 1205, 1209, 1210 raised by pass 9, which the triage never read.

## Note
Only the 1029 commit exists (99158a4b). My standing instructions forbid git writes, so the rest is uncommitted in the worktree.
