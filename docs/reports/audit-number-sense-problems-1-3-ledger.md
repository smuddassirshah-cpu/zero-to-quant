# Claim ledger: number-sense problems-1 to problems-3 (blind concept audit)

Stage 0 depth: every graded key, wrong option and slip, each stated rule or comparison, and each value carried between parts. Written by `docs/reports/number-sense-problems-concepts.py --ledger`; the basis column is the exact-fraction derivation the script asserts.

Rows: 253. correct 243, imprecise 10.

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| problems-1 | items[0].parts[0].widget.answer | key 5 = 5 | correct | 1/4 of 20 |
| problems-1 | items[0].parts[0].widget.wrong (set) | every slip is in the audit table | correct | coverage |
| problems-1 | items[0].parts[0].widget.wrong.flipped | slip 80 is the named mistake (80) and never the key | correct | 20 x 4 |
| problems-1 | items[0].parts[0].widget.wrong.three-quarters | slip 15 is the named mistake (15) and never the key | correct | 3/4 of 20 |
| problems-1 | items[0].parts[1].widget.answer | key 0.65 = 13/20 | correct | 2/5 + 1/4 = 8/20 + 5/20 |
| problems-1 | items[0].parts[1].widget.wrong (set) | every slip is in the audit table | correct | coverage |
| problems-1 | items[0].parts[1].widget.wrong.tops-bottoms | slip 0.333333 is the named mistake (1/3) and never the key | correct | (2+1)/(5+4) = 3/9 |
| problems-1 | items[0].parts[1].widget.wrong.tops-kept | slip 0.15 is the named mistake (3/20) and never the key | correct | 2/20 + 1/20 |
| problems-1 | items[0].parts[2].widget.answer | key 0.35 = 7/20 | correct | 1 - 13/20 (carried value) |
| problems-1 | items[0].parts[2].widget.wrong (set) | every slip is in the audit table | correct | coverage |
| problems-1 | items[0].parts[2].widget.wrong.carried | slip 0.666667 is the named mistake (2/3) and never the key | correct | 1 - 3/9, the part 2 slip |
| problems-1 | items[0].parts[2].widget.wrong.beds | slip 7 is the named mistake (7) and never the key | correct | 7/20 of 20 beds |
| problems-1 | items[0].parts[3].widget.answer | key 0.175 = 7/40 | correct | 1/2 x 7/20 (carried value) |
| problems-1 | items[0].parts[3].widget.wrong (set) | every slip is in the audit table | correct | coverage |
| problems-1 | items[0].parts[3].widget.wrong.doubled | slip 0.7 is the named mistake (7/10) and never the key | correct | 2 x 7/20 |
| problems-1 | items[0].parts[3].widget.wrong.added-half | slip 0.85 is the named mistake (17/20) and never the key | correct | 1/2 + 7/20 |
| problems-1 | items[0].parts[3].widget.wrong.carried | slip 0.333333 is the named mistake (1/3) and never the key | correct | 1/2 x 2/3, the carried slip |
| problems-1 | items[1].parts[0].widget.answer | key 4.166667 = 25/6 | imprecise | 5/6 / 1/5 = 25/6; finding 2: exact form asked, window takes 3 d.p. and rejects 2 d.p. |
| problems-1 | items[1].parts[0].widget.wrong (set) | every slip is in the audit table | correct | coverage |
| problems-1 | items[1].parts[0].widget.wrong.multiplied | slip 0.166667 is the named mistake (1/6) and never the key | correct | 5/6 x 1/5 |
| problems-1 | items[1].parts[0].widget.wrong.wrong-flip | slip 0.24 is the named mistake (6/25) and never the key | correct | 6/5 x 1/5 |
| problems-1 | items[1].parts[1].widget.answer | key 4 = 4 | correct | floor(4 1/6) |
| problems-1 | items[1].parts[1].widget.wrong (set) | every slip is in the audit table | correct | coverage |
| problems-1 | items[1].parts[1].widget.wrong.rounded-up | slip 5 is the named mistake (5) and never the key | correct | ceil(4 1/6) |
| problems-1 | items[1].parts[1].widget.wrong.carried | slip 0 is the named mistake (0) and never the key | correct | floor(1/6); floor(6/25) is 0 too |
| problems-1 | items[1].parts[2].widget.answer | key 0.033333 = 1/30 | imprecise | 5/6 - 4/5 = 1/30; finding 2: exact form asked, window takes 3 d.p. and rejects 2 d.p. |
| problems-1 | items[1].parts[2].widget.wrong (set) | every slip is in the audit table | correct | coverage |
| problems-1 | items[1].parts[2].widget.wrong.one-loaf | slip 0.633333 is the named mistake (19/30) and never the key | correct | 5/6 - 1/5 |
| problems-1 | items[1].parts[2].widget.wrong.tops-bottoms | slip 1 is the named mistake (1) and never the key | correct | (5-4)/(6-5) |
| problems-1 | items[1].parts[2].widget.wrong.loaf-sixth | slip 0.166667 is the named mistake (1/6) and never the key | correct | fraction part of 4 1/6 |
| problems-1 | items[1].parts[3].widget.answer | key 0.04 = 1/25 | correct | 1/30 / 5/6 = 1/25 |
| problems-1 | items[1].parts[3].widget.wrong (set) | every slip is in the audit table | correct | coverage |
| problems-1 | items[1].parts[3].widget.wrong.multiplied | slip 0.027778 is the named mistake (1/36) and never the key | correct | 1/30 x 5/6 |
| problems-1 | items[1].parts[3].widget.wrong.flipped | slip 25 is the named mistake (25) and never the key | correct | 5/6 / 1/30 |
| problems-1 | items[1].parts[3].widget.wrong.carried | slip 0.76 is the named mistake (19/25) and never the key | correct | 19/30 / 5/6, the one-loaf slip |
| problems-1 | items[2].parts[0].widget.answer | key 0.708333 = 17/24 | imprecise | 3/8 + 1/3 = 9/24 + 8/24; finding 2: exact form asked, window takes 3 d.p. and rejects 2 d.p. |
| problems-1 | items[2].parts[0].widget.wrong (set) | every slip is in the audit table | correct | coverage |
| problems-1 | items[2].parts[0].widget.wrong.tops-bottoms | slip 0.363636 is the named mistake (4/11) and never the key | correct | (3+1)/(8+3) |
| problems-1 | items[2].parts[0].widget.wrong.multiplied | slip 0.125 is the named mistake (1/8) and never the key | correct | 3/8 x 1/3 |
| problems-1 | items[2].parts[1].widget.answer | key 0.291667 = 7/24 | imprecise | 1 - 17/24; finding 2: exact form asked, window takes 3 d.p. and rejects 2 d.p. |
| problems-1 | items[2].parts[1].widget.wrong (set) | every slip is in the audit table | correct | coverage |
| problems-1 | items[2].parts[1].widget.wrong.carried | slip 0.636364 is the named mistake (7/11) and never the key | correct | 1 - 4/11, the part 1 slip |
| problems-1 | items[2].parts[1].widget.wrong.count | slip 7 is the named mistake (7) and never the key | correct | number of twenty-fourths |
| problems-1 | items[2].parts[2].widget.answer | key 0.777778 = 7/9 | imprecise | 7/24 / 3/8 = 7/9 h; finding 2: exact form asked, window takes 3 d.p. and rejects 2 d.p. |
| problems-1 | items[2].parts[2].widget.wrong (set) | every slip is in the audit table | correct | coverage |
| problems-1 | items[2].parts[2].widget.wrong.multiplied | slip 0.109375 is the named mistake (7/64) and never the key | correct | 7/24 x 3/8 |
| problems-1 | items[2].parts[2].widget.wrong.flipped | slip 1.285714 is the named mistake (9/7) and never the key | correct | 3/8 / 7/24 |
| problems-1 | items[2].parts[2].widget.wrong.printer-b | slip 0.875 is the named mistake (7/8) and never the key | correct | 7/24 / 1/3 |
| problems-1 | items[2].parts[2].widget.wrong.minutes | slip 46.666667 is the named mistake (140/3) and never the key | correct | 7/9 h in minutes |
| problems-1 | items[2].parts[3].widget.answer | key 106.666667 = 320/3 | imprecise | 60 + 7/9 x 60 = 320/3 min; finding 2: exact form asked, window takes 3 d.p. and rejects 2 d.p. |
| problems-1 | items[2].parts[3].widget.wrong (set) | every slip is in the audit table | correct | coverage |
| problems-1 | items[2].parts[3].widget.wrong.rest-only | slip 46.666667 is the named mistake (140/3) and never the key | correct | 7/9 x 60 |
| problems-1 | items[2].parts[3].widget.wrong.hundred | slip 177.777778 is the named mistake (1600/9) and never the key | correct | 100 + 7/9 x 100 |
| problems-1 | items[2].parts[3].widget.wrong.carried-flipped | slip 137.142857 is the named mistake (960/7) and never the key | correct | 60 + 9/7 x 60 |
| problems-1 | items[2].parts[3].widget.wrong.hours | slip 1.777778 is the named mistake (16/9) and never the key | correct | 1 7/9 h |
| problems-1 | items[3].parts[0].widget.answer | key 16 = 16 | correct | 4/9 = 16/36 |
| problems-1 | items[3].parts[0].widget.wrong (set) | every slip is in the audit table | correct | coverage |
| problems-1 | items[3].parts[0].widget.wrong.top-kept | slip 4 is the named mistake (4) and never the key | correct | top left at 4 |
| problems-1 | items[3].parts[0].widget.wrong.added | slip 31 is the named mistake (31) and never the key | correct | 4 + 27 |
| problems-1 | items[3].parts[0].widget.wrong.whole-fraction | slip 0.444444 is the named mistake (4/9) and never the key | correct | 16/36 typed whole |
| problems-1 | items[3].parts[1].widget.options (key) | correct option is a | correct | recomputed comparison |
| problems-1 | items[3].parts[1].widget.options (set) | every wrong option is in the audit table | correct | coverage |
| problems-1 | items[3].parts[1].widget.options.b-top | option is wrong under every reading | correct | 15/36 < 16/36, so B is weaker |
| problems-1 | items[3].parts[1].widget.options.same | option is wrong under every reading | correct | 15/36 != 16/36 |
| problems-1 | items[3].parts[2].widget.answer | key 0.333333 = 1/3 | imprecise | 4/9 x 3/4 = 1/3 l; finding 2: exact form asked, window takes 3 d.p. and rejects 2 d.p. |
| problems-1 | items[3].parts[2].widget.wrong (set) | every slip is in the audit table | correct | coverage |
| problems-1 | items[3].parts[2].widget.wrong.added | slip 1.194444 is the named mistake (43/36) and never the key | correct | 4/9 + 3/4 = 43/36 |
| problems-1 | items[3].parts[2].widget.wrong.divided | slip 0.592593 is the named mistake (16/27) and never the key | correct | 4/9 / 3/4 = 16/27 |
| problems-1 | items[3].parts[3].widget.answer | key 0.645833 = 31/48 | imprecise | 1/3 + 5/16 = 31/48 l; finding 2: exact form asked, window takes 3 d.p. and rejects 2 d.p. |
| problems-1 | items[3].parts[3].widget.wrong (set) | every slip is in the audit table | correct | coverage |
| problems-1 | items[3].parts[3].widget.wrong.tops-bottoms | slip 0.315789 is the named mistake (6/19) and never the key | correct | (1+5)/(3+16) |
| problems-1 | items[3].parts[3].widget.wrong.carried | slip 1.506944 is the named mistake (217/144) and never the key | correct | 43/36 + 5/16, the part 3 slip |
| problems-1 | items[3].parts[4].widget.answer | key 0.430556 = 31/72 | imprecise | 31/48 / 3/2 = 31/72; finding 2: exact form asked, window takes 3 d.p. and rejects 2 d.p. |
| problems-1 | items[3].parts[4].widget.wrong (set) | every slip is in the audit table | correct | coverage |
| problems-1 | items[3].parts[4].widget.wrong.multiplied | slip 0.96875 is the named mistake (31/32) and never the key | correct | 31/48 x 3/2 |
| problems-1 | items[3].parts[4].widget.wrong.shares-added | slip 0.861111 is the named mistake (31/36) and never the key | correct | 4/9 + 5/12 = 31/36 |
| problems-2 | items[0].parts[0].widget.answer | key 1.3 = 13/10 | correct | -3.6 + 4.9 |
| problems-2 | items[0].parts[0].widget.wrong (set) | every slip is in the audit table | correct | coverage |
| problems-2 | items[0].parts[0].widget.wrong.subtracted | slip -8.5 is the named mistake (-17/2) and never the key | correct | -3.6 - 4.9 |
| problems-2 | items[0].parts[0].widget.wrong.start-sign | slip 8.5 is the named mistake (17/2) and never the key | correct | 3.6 + 4.9 |
| problems-2 | items[0].parts[1].widget.answer | key -6.3 = -63/10 | correct | -5 - 1.3 (end minus start) |
| problems-2 | items[0].parts[1].widget.wrong (set) | every slip is in the audit table | correct | coverage |
| problems-2 | items[0].parts[1].widget.wrong.sign | slip 6.3 is the named mistake (63/10) and never the key | correct | size without the minus |
| problems-2 | items[0].parts[1].widget.wrong.added | slip -3.7 is the named mistake (-37/10) and never the key | correct | -5 + 1.3 |
| problems-2 | items[0].parts[1].widget.wrong.carried | slip 3.5 is the named mistake (7/2) and never the key | correct | -5 - (-8.5), the part 1 slip |
| problems-2 | items[0].parts[2].widget.answer | key -0.7 = -7/10 | correct | -6.3 / 9 |
| problems-2 | items[0].parts[2].widget.wrong (set) | every slip is in the audit table | correct | coverage |
| problems-2 | items[0].parts[2].widget.wrong.sign | slip 0.7 is the named mistake (7/10) and never the key | correct | sign dropped |
| problems-2 | items[0].parts[2].widget.wrong.times | slip -56.7 is the named mistake (-567/10) and never the key | correct | -6.3 x 9 |
| problems-2 | items[0].parts[3].widget.answer | key -7.8 = -39/5 | correct | -5 + 4 x (-0.7) |
| problems-2 | items[0].parts[3].widget.wrong (set) | every slip is in the audit table | correct | coverage |
| problems-2 | items[0].parts[3].widget.wrong.sign | slip 7.8 is the named mistake (39/5) and never the key | correct | sign dropped |
| problems-2 | items[0].parts[3].widget.wrong.minus-minus | slip -2.2 is the named mistake (-11/5) and never the key | correct | -5 - (-2.8) |
| problems-2 | items[0].parts[3].widget.wrong.change-only | slip -2.8 is the named mistake (-14/5) and never the key | correct | 4 x (-0.7) |
| problems-2 | items[1].parts[0].widget.answer | key -1 = -1 | correct | 4(-1) + (-2) + 3(1) + 2 |
| problems-2 | items[1].parts[0].widget.wrong (set) | every slip is in the audit table | correct | coverage |
| problems-2 | items[1].parts[0].widget.wrong.sign | slip 1 is the named mistake (1) and never the key | correct | sign flipped |
| problems-2 | items[1].parts[0].widget.wrong.eagle-one | slip 0 is the named mistake (0) and never the key | correct | eagle counted as -1 |
| problems-2 | items[1].parts[0].widget.wrong.no-signs | slip 11 is the named mistake (11) and never the key | correct | sizes added |
| problems-2 | items[1].parts[1].widget.answer | key -2 = -2 | correct | (-1 + 2 - 6 - 3) / 4 |
| problems-2 | items[1].parts[1].widget.wrong (set) | every slip is in the audit table | correct | coverage |
| problems-2 | items[1].parts[1].widget.wrong.sign | slip 2 is the named mistake (2) and never the key | correct | sign dropped |
| problems-2 | items[1].parts[1].widget.wrong.plus-as-minus | slip -3 is the named mistake (-3) and never the key | correct | +2 read as -2 |
| problems-2 | items[1].parts[1].widget.wrong.total | slip -8 is the named mistake (-8) and never the key | correct | total, not shared |
| problems-2 | items[1].parts[2].widget.answer | key 0.278 = 139/500 | correct | 5/18 = 0.2777.. to 3 d.p. |
| problems-2 | items[1].parts[2].widget.wrong (set) | every slip is in the audit table | correct | coverage |
| problems-2 | items[1].parts[2].widget.wrong.unrounded | slip 0.277778 is the named mistake (138889/500000) and never the key | correct | 5/18 to 6 d.p. |
| problems-2 | items[1].parts[2].widget.wrong.truncated | slip 0.277 is the named mistake (277/1000) and never the key | correct | cut at 3 d.p. |
| problems-2 | items[1].parts[2].widget.wrong.flipped | slip 3.6 is the named mistake (18/5) and never the key | correct | 18 / 5 |
| problems-2 | items[1].parts[2].widget.answer (convention) | alternative 0.278 is marked right, not caught by a slip | correct | half-even or half-up, same 0.278 |
| problems-2 | items[1].parts[3].widget.options (key) | correct option is rival | correct | recomputed comparison |
| problems-2 | items[1].parts[3].widget.options (set) | every wrong option is in the audit table | correct | coverage |
| problems-2 | items[1].parts[3].widget.options.golfer | option is wrong under every reading | correct | 5/18 < 0.28 (gap 1/450) |
| problems-2 | items[1].parts[3].widget.options.same | option is wrong under every reading | correct | 5/18 != 7/25 |
| problems-2 | items[2].parts[0].widget.answer | key 2.8333 = 28333/10000 | correct | 17/6 to 4 d.p. |
| problems-2 | items[2].parts[0].widget.wrong (set) | every slip is in the audit table | correct | coverage |
| problems-2 | items[2].parts[0].widget.wrong.flipped | slip 0.3529 is the named mistake (3529/10000) and never the key | correct | 6/17 to 4 d.p. |
| problems-2 | items[2].parts[0].widget.wrong.remainder | slip 2.5 is the named mistake (5/2) and never the key | correct | 2 r 5 read as 2.5 |
| problems-2 | items[2].parts[1].widget.answer | key 2.83 = 283/100 | correct | 2.8333 to 2 d.p. |
| problems-2 | items[2].parts[1].widget.wrong (set) | every slip is in the audit table | correct | coverage |
| problems-2 | items[2].parts[1].widget.wrong.unrounded | slip 2.8333 is the named mistake (28333/10000) and never the key | correct | not rounded |
| problems-2 | items[2].parts[1].widget.wrong.rounded-up | slip 2.84 is the named mistake (71/25) and never the key | correct | rounded up |
| problems-2 | items[2].parts[1].widget.wrong.one-dp | slip 2.8 is the named mistake (14/5) and never the key | correct | 1 d.p. |
| problems-2 | items[2].parts[1].widget.wrong.pence | slip 283 is the named mistake (283) and never the key | correct | in pence |
| problems-2 | items[2].parts[2].widget.answer | key -2 = -2 | correct | 6 x 283 - 1700 pence |
| problems-2 | items[2].parts[2].widget.wrong (set) | every slip is in the audit table | correct | coverage |
| problems-2 | items[2].parts[2].widget.wrong.sign | slip 2 is the named mistake (2) and never the key | correct | fare minus collected |
| problems-2 | items[2].parts[2].widget.wrong.pounds | slip -0.02 is the named mistake (-1/50) and never the key | correct | in pounds |
| problems-2 | items[2].parts[2].widget.wrong.carried-up | slip 4 is the named mistake (4) and never the key | correct | 6 x 284 - 1700, the 2.84 slip |
| problems-2 | items[2].parts[3].widget.answer | key 2.85 = 57/20 | correct | 17 - 5 x 2.83 |
| problems-2 | items[2].parts[3].widget.wrong (set) | every slip is in the audit table | correct | coverage |
| problems-2 | items[2].parts[3].widget.wrong.same | slip 2.83 is the named mistake (283/100) and never the key | correct | a plain share |
| problems-2 | items[2].parts[3].widget.wrong.wrong-way | slip 2.81 is the named mistake (281/100) and never the key | correct | 2.83 - 0.02 |
| problems-2 | items[2].parts[3].widget.wrong.shortfall | slip 0.02 is the named mistake (1/50) and never the key | correct | the gap alone |
| problems-2 | items[2].parts[3].widget.wrong.pence | slip 285 is the named mistake (285) and never the key | correct | in pence |
| problems-2 | items[2].parts[3].widget.answer (convention) | alternative 2.85 is marked right, not caught by a slip | correct | share plus shortfall |
| problems-3 | items[0].parts[0].widget.answer | key 12 = 12 | correct | largest n with n^3 <= 2169 |
| problems-3 | items[0].parts[0].widget.wrong (set) | every slip is in the audit table | correct | coverage |
| problems-3 | items[0].parts[0].widget.wrong.rounded-up | slip 13 is the named mistake (13) and never the key | correct | 13, but 13^3 = 2197 > 2169 |
| problems-3 | items[0].parts[0].widget.wrong.square-root | slip 46 is the named mistake (46) and never the key | correct | sqrt(2169) = 46.57; window 45 to 47 |
| problems-3 | items[0].parts[0].widget.wrong.thirds | slip 723 is the named mistake (723) and never the key | correct | 2169 / 3 |
| problems-3 | items[0].parts[1].widget.answer | key 441 = 441 | correct | 2169 - 1728 |
| problems-3 | items[0].parts[1].widget.wrong (set) | every slip is in the audit table | correct | coverage |
| problems-3 | items[0].parts[1].widget.wrong.squared | slip 2025 is the named mistake (2025) and never the key | correct | 2169 - 144 |
| problems-3 | items[0].parts[1].widget.wrong.carried-up | slip -28 is the named mistake (-28) and never the key | correct | 2169 - 2197 |
| problems-3 | items[0].parts[1].widget.wrong.times-three | slip 2133 is the named mistake (2133) and never the key | correct | 2169 - 36 |
| problems-3 | items[0].parts[2].widget.answer | key 21 = 21 | correct | sqrt(441) |
| problems-3 | items[0].parts[2].widget.wrong (set) | every slip is in the audit table | correct | coverage |
| problems-3 | items[0].parts[2].widget.wrong.halved | slip 220.5 is the named mistake (441/2) and never the key | correct | 441 / 2 |
| problems-3 | items[0].parts[2].widget.wrong.quartered | slip 110.25 is the named mistake (441/4) and never the key | correct | 441 / 4 |
| problems-3 | items[1].parts[0].widget.answer | key 220 = 220 | correct | 40 x 5 + 20 |
| problems-3 | items[1].parts[0].widget.wrong (set) | every slip is in the audit table | correct | coverage |
| problems-3 | items[1].parts[0].widget.wrong.bracket-first | slip 1000 is the named mistake (1000) and never the key | correct | 40 x (5 + 20) |
| problems-3 | items[1].parts[0].widget.wrong.no-delivery | slip 200 is the named mistake (200) and never the key | correct | 40 x 5 |
| problems-3 | items[1].parts[0].widget.answer (convention) | alternative 220 is marked right, not caught by a slip | correct | product rounded again |
| problems-3 | items[1].parts[1].widget.answer | key 203.8 = 1019/5 | correct | 38 x 4.85 + 19.50 |
| problems-3 | items[1].parts[1].widget.wrong (set) | every slip is in the audit table | correct | coverage |
| problems-3 | items[1].parts[1].widget.wrong.bracket | slip 925.3 is the named mistake (9253/10) and never the key | correct | 38 x (4.85 + 19.50) |
| problems-3 | items[1].parts[1].widget.wrong.boxes-only | slip 184.3 is the named mistake (1843/10) and never the key | correct | 38 x 4.85 |
| problems-3 | items[1].parts[2].widget.answer | key 190.8 = 954/5 | correct | 38 x 4.85 + (19.50 / 3) |
| problems-3 | items[1].parts[2].widget.wrong (set) | every slip is in the audit table | correct | coverage |
| problems-3 | items[1].parts[2].widget.wrong.intended | slip 67.93 is the named mistake (6793/100) and never the key | correct | (bill) / 3 to the penny |
| problems-3 | items[1].parts[2].widget.wrong.delivery-share | slip 6.5 is the named mistake (13/2) and never the key | correct | 19.50 / 3 |
| problems-3 | items[1].parts[2].widget.answer (convention) | alternative 190.8 is marked right, not caught by a slip | correct | left to right gives the same, x before + |
| problems-3 | items[1].parts[3].widget.answer | key 67.93 = 6793/100 | correct | 203.80 / 3 to the penny |
| problems-3 | items[1].parts[3].widget.wrong (set) | every slip is in the audit table | correct | coverage |
| problems-3 | items[1].parts[3].widget.wrong.calculator | slip 190.8 is the named mistake (954/5) and never the key | correct | the part 3 display |
| problems-3 | items[1].parts[3].widget.wrong.carried-bracket | slip 308.43 is the named mistake (30843/100) and never the key | correct | 925.30 / 3 |
| problems-3 | items[1].parts[3].widget.wrong.estimate | slip 73.33 is the named mistake (7333/100) and never the key | correct | 220 / 3 |
| problems-3 | items[2].parts[0].widget.answer | key 30000 = 30000 | correct | 1.2e9 / 4e4 |
| problems-3 | items[2].parts[0].widget.wrong (set) | every slip is in the audit table | correct | coverage |
| problems-3 | items[2].parts[0].widget.wrong.kept-point | slip 300000 is the named mistake (300000) and never the key | correct | 3 x 10^5 |
| problems-3 | items[2].parts[0].widget.wrong.added-indices | slip 3000000000000.0 is the named mistake (3000000000000) and never the key | correct | 0.3 x 10^(9+4) |
| problems-3 | items[2].parts[0].widget.wrong.short | slip 3000 is the named mistake (3000) and never the key | correct | 3 x 10^3 |
| problems-3 | items[2].parts[1].widget.answer | key 9000 = 9000 | correct | 8760 to 1 s.f. |
| problems-3 | items[2].parts[1].widget.wrong (set) | every slip is in the audit table | correct | coverage |
| problems-3 | items[2].parts[1].widget.wrong.truncated | slip 8000 is the named mistake (8000) and never the key | correct | digits cut |
| problems-3 | items[2].parts[1].widget.wrong.two-sf | slip 8800 is the named mistake (8800) and never the key | correct | 2 s.f. |
| problems-3 | items[2].parts[2].widget.answer | key 3 = 3 | correct | 30000 / 9000 to 1 s.f. |
| problems-3 | items[2].parts[2].widget.wrong (set) | every slip is in the audit table | correct | coverage |
| problems-3 | items[2].parts[2].widget.wrong.inverted | slip 0.3 is the named mistake (3/10) and never the key | correct | 9000 / 30000 |
| problems-3 | items[2].parts[2].widget.wrong.carried | slip 4 is the named mistake (4) and never the key | correct | 30000 / 8000 = 3.75 to 1 s.f. |
| problems-3 | items[2].parts[2].widget.wrong.unrounded | slip 3.33 is the named mistake (333/100) and never the key | correct | 3.33, not rounded |
| problems-3 | items[2].parts[2].widget.answer (convention) | alternative 3 is marked right, not caught by a slip | correct | unrounded year, still 3 |
| problems-3 | items[2].parts[2].widget.answer (convention) | alternative 3 is marked right, not caught by a slip | correct | 2 s.f. year, still 3 |
| problems-3 | items[2].parts[3].widget.answer | key 3.4 = 17/5 | correct | 30000 / 8760 to 1 d.p. |
| problems-3 | items[2].parts[3].widget.wrong (set) | every slip is in the audit table | correct | coverage |
| problems-3 | items[2].parts[3].widget.wrong.nine-thousand | slip 3.3 is the named mistake (33/10) and never the key | correct | 30000 / 9000 |
| problems-3 | items[2].parts[3].widget.wrong.carried | slip 34.2 is the named mistake (171/5) and never the key | correct | 300000 / 8760 |
| problems-3 | items[2].parts[3].widget.wrong.days | slip 1250 is the named mistake (1250) and never the key | correct | 30000 / 24 |
| problems-3 | items[2].parts[3].widget.answer (convention) | alternative 3.4 is marked right, not caught by a slip | correct | 365.25-day year, still 3.4 |
| problems-1 | items[0].parts[3].explain | 7/40 of 20 beds is three and a half beds | correct | 7/40 x 20 |
| problems-1 | items[1].parts[0].explain | dividing by 1/5 is multiplying by 5 | correct | reciprocal |
| problems-1 | items[1].parts[1].feedback.byKey.rounded-up | the flour left is a sixth of a loaf | correct | 1/30 / 1/5 |
| problems-1 | items[1].parts[2].feedback.byKey.loaf-sixth | a sixth of 1/5 kg is 1/30 kg | correct | product |
| problems-1 | items[1].parts[3].explain | a fraction of the start is leftover divided by start | correct | definition of a share |
| problems-1 | items[2].parts[0].feedback.byKey.tops-bottoms | 4/11 is less than A prints alone | correct | 32/88 < 33/88 |
| problems-1 | items[2].parts[1].explain | 7/24 is a little under a third | correct | 7/24 < 8/24 |
| problems-1 | items[2].parts[2].explain | 7/24 is 7 of the 9 pieces A does in an hour | correct | 3/8 = 9/24 |
| problems-1 | items[2].parts[3].feedback.correct | 7/9 of 60 min is 420/9 = 46 2/3 | correct | exact |
| problems-1 | items[3].parts[1].widget.options[1].why | ninths are bigger than twelfths | correct | 1/9 > 1/12 |
| problems-1 | items[3].parts[1].widget.options[2].why | both shares are under a half | correct | 16, 15 < 18 thirty-sixths |
| problems-1 | items[3].parts[2].explain | 1/3 is less than either fraction multiplied | correct | product of proper fractions |
| problems-1 | items[3].parts[3].question | 5/12 x 3/4 = 5/16 | correct | 15/48 |
| problems-1 | items[3].parts[3].feedback.byKey.tops-bottoms | 6/19 is less than jug A alone | correct | 18/57 < 19/57 |
| problems-1 | items[3].parts[4].question | two 3/4 l jugs make 3/2 l | correct | sum |
| problems-1 | items[3].parts[4].feedback.byKey.shares-added | bowl share is half the sum of the shares (equal jugs) | correct | equal volumes, so the mean |
| problems-1 | items[3].parts[4].explain | the mix sits between the two jug shares | correct | 30/72 < 31/72 < 32/72 |
| problems-2 | items[0].parts[0].explain | 3.6 up to zero, then 1.3 more | correct | number line |
| problems-2 | items[0].parts[1].question | 2 pm to 11 pm is 9 hours | correct | clock |
| problems-2 | items[0].parts[2].explain | negative divided by positive is negative | correct | sign rule |
| problems-2 | items[0].parts[3].question | 4 hours after 11 pm is 3 am | correct | clock |
| problems-2 | items[1].prose | the card has 18 holes | correct | count |
| problems-2 | items[1].parts[0].feedback.byKey.sign | 6 shots under and 5 over | correct | count |
| problems-2 | items[1].parts[2].question | under par on 5 of 18 holes | correct | 4 birdies and 1 eagle |
| problems-2 | items[1].parts[3].widget.options[2].why | 0.2777.. is below 0.28 by about 0.002 | correct | 1/450 = 0.00222 |
| problems-2 | items[2].parts[0].explain | 17/6: 2 r 5, 50 -> 8 r 2, 20 -> 3 r 2 recurring | correct | long division |
| problems-2 | items[2].parts[2].feedback.byKey.sign | six pay 16.98 | correct | product |
| problems-2 | items[2].parts[3].explain | 5 x 2.83 = 14.15 and 2.85 = 2.83 + 0.02 | correct | exact |
| problems-3 | items[0].parts[0].explain | 12^3 = 1728 < 2169 < 2197 = 13^3 | correct | cubes |
| problems-3 | items[0].parts[2].explain | 20^2 = 400, 22^2 = 484, 21^2 = 441 | correct | squares |
| problems-3 | items[1].parts[0].feedback.correct | 38 -> 40, 4.85 -> 5, 19.50 -> 20 at 1 s.f. | correct | rounding |
| problems-3 | items[1].parts[1].feedback.correct | 38 x 4.85 = 184.30 | correct | product |
| problems-3 | items[1].parts[2].explain | x and / before +; a share is about 73 | correct | order of operations (stated convention) |
| problems-3 | items[1].parts[3].explain | 203.80 / 3 = 67.9333.., third decimal 3 | correct | division |
| problems-3 | items[2].parts[0].feedback.correct | 0.3 x 10^5 = 3 x 10^4; dividing powers subtracts indices | correct | index law |
| problems-3 | items[2].parts[1].question | 24 x 365 = 8760 | correct | product; 365-day year stated |
| problems-3 | items[2].parts[3].explain | 3.42.. exceeds 3.33.. because 8760 < 9000 | correct | smaller divisor, larger quotient |
| problems-3 | items[2].parts[3].feedback.byKey.days | 30000 / 24 = 1250 days | correct | division |
| problems-2 | items[1].parts[3].question | finding 1: 0.28 of an 18-hole round is not a whole number of holes, and 5/18 is 0.28 to 2 d.p. | imprecise | see audit file |
| chain | carry[0] | value carried forward 13/20 equals the earlier key | correct | recomputed |
| chain | carry[1] | value carried forward 7/20 equals the earlier key | correct | recomputed |
| chain | carry[2] | value carried forward 25/6 equals the earlier key | correct | recomputed |
| chain | carry[3] | value carried forward 4 equals the earlier key | correct | recomputed |
| chain | carry[4] | value carried forward 1/30 equals the earlier key | correct | recomputed |
| chain | carry[5] | value carried forward 17/24 equals the earlier key | correct | recomputed |
| chain | carry[6] | value carried forward 7/24 equals the earlier key | correct | recomputed |
| chain | carry[7] | value carried forward 7/9 equals the earlier key | correct | recomputed |
| chain | carry[8] | value carried forward 16 equals the earlier key | correct | recomputed |
| chain | carry[9] | value carried forward 1/3 equals the earlier key | correct | recomputed |
| chain | carry[10] | value carried forward 31/48 equals the earlier key | correct | recomputed |
| chain | carry[11] | value carried forward 13/10 equals the earlier key | correct | recomputed |
| chain | carry[12] | value carried forward -63/10 equals the earlier key | correct | recomputed |
| chain | carry[13] | value carried forward -7/10 equals the earlier key | correct | recomputed |
| chain | carry[14] | value carried forward -1 equals the earlier key | correct | recomputed |
| chain | carry[15] | value carried forward 28333/10000 equals the earlier key | correct | recomputed |
| chain | carry[16] | value carried forward 283/100 equals the earlier key | correct | recomputed |
| chain | carry[17] | value carried forward -2 equals the earlier key | correct | recomputed |
| chain | carry[18] | value carried forward 12 equals the earlier key | correct | recomputed |
| chain | carry[19] | value carried forward 441 equals the earlier key | correct | recomputed |
| chain | carry[20] | value carried forward 1019/5 equals the earlier key | correct | recomputed |
| chain | carry[21] | value carried forward 30000 equals the earlier key | correct | recomputed |
| chain | carry[22] | value carried forward 9000 equals the earlier key | correct | recomputed |
