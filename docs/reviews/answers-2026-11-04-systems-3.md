# Answer check, systems level 3, 4 November 2026

**Summary.** 72 items checked: l11 (10 screens, 4 quiz), l12 (9, 4), l13 (11, 4), l14 (10, 4), review-3 (9), homework-3 (7 items, 15 graded parts, 1 longform). That covers 60 table cells, every `wrong` value, every choice option and every quoted figure. Wrong keys: 0. Other mismatches: 1 repeat of a lesson's numbers, 5 sentences of 20 words, 7 choice keys visibly longer than their distractors, 5 fresh-number notes (none wrong). The fresh-number rule is in DECISIONS "Fresh numbers in reviews and homework".

I recomputed everything in my own scripts before reading `docs/reports/systems-3.md` (not read at all). Scripts are in `/tmp/claude-0/-home-user-zero-to-quant/024bfe09-7a97-56c3-837c-b47a15727adf/scratchpad/answers-systems-3/`:

- `nums.py` recomputes every numeric, table, `wrong` and quoted figure, and decodes `feed.hex` with `struct`.
- `cpp.py` builds each C++ item into a harness and compiles it with `clang++ -std=c++17 -O1 -fno-exceptions`. It runs the reference solution and the starter against every hidden test.
- `voice.py` checks dashes, exclamation marks, sentences of 20 words or more and explanations over 3 sentences.
- `choice.py` compares key and distractor lengths and checks `wrong` bands for overlap and missing `byKey` lines.
- `dups.py` and grep cover the duplicate search.

Engine note: a numeric cell with `unit: "%"` takes the answer as a fraction (AUTHORING line 121), so 0.4 is 40%, 0.04 is 4%, 0.675 is 67.5%. I read every such key that way.

## Per item

### l11-processes

| Item | Key | Computation | Verdict |
|---|---|---|---|
| s0 tap `recvfrom` | l3 | 0.012340 s is 12.34 ms against 8 to 12 µs; ratio 1,028 to 1,542 ("over a thousand") | ok; byKey l1, l2, l4 quote their times correctly |
| s1 calls at 64 KiB | 16 | 1,048,576 / 65,536; wrong 16384 is 64 B reads, 256 is 4 KiB reads; 3.2 µs and 3,276.8 µs, 1,024 times | ok |
| s2 table | 16384, 3276.8, 256, 51.2, 1024 | 1,048,576/64; x0.2; /4096; x0.2; 16384/16 | ok |
| s3 table | 2, 4, 40% | 2 switches x 2 µs = 4 µs; 100,000 x 4 µs = 0.4 s | ok |
| s4 fork | own (still 5) | copy-on-write; distractors shared, early, race are wrong as written | ok |
| s5 call vs switch | no | 16,384 x 0.2 µs = 3.28 ms ("about 3.3 ms"); 2 µs vs 0.2 µs is ten times | ok |
| s6 clock | 10 ms | 500,000 x 20 ns = 10 ms; kernel 100 ms; slip 1 is one power of ten low | ok |
| s7 halve | half | overhead goes as 1/size | ok |
| s8 drill | 1024, 204.8, 128, 25.6, 1.0 | 4 MiB/4 KiB; x0.2; 8 MiB/64 KiB; x0.2; 250,000 x 4 µs = 1 s | ok |
| s9 follow-up | 40 ms, 4%, 3279 | 200,000 x 0.2 µs = 40 ms = 4%; 200,000/61 = 3,278.7 (tol 1); 61 = floor(1472/24), 8 spare; 3,279 x 0.2 µs = 0.066% ("about 0.07%") | ok |
| q-overhead | 12.8 | 2 MiB/32 KiB = 64 calls x 0.2; wrong 64 | ok |
| q-shortcut | clock | the others are system calls | ok |
| q-fd | yes | table shared by threads | ok |
| q-wake | 20% | 50,000 x 4 µs = 0.2 s; wrong 0.1 is one switch | ok |

### l12-files-and-sockets

| Item | Key | Computation | Verdict |
|---|---|---|---|
| s0 order | s1 to s7 | card, card signals, stack finds socket, buffer and wake, scheduler, copy, return | ok (one defensible order) |
| s1 budgets | 2 | 10/5; bypass 1/5 = 0.2; half 0.5 is 5/10 | ok |
| s2 table | 4, 4, 41, 16 | divmod(100,24) = (4,4); divmod(1000,24) = (41,16) | ok |
| s3 table | 5, 0.2, 250, 100% | 50/0.2 = 250; a loop that never sleeps is 1.0 | ok |
| s4 short read | ready | read returns what is ready; -1 error, 0 closed | ok |
| s5 zero | spin | recv returns 0 at once after a close; `continue` retries | ok |
| s6 handler | keep | keep the remainder | ok |
| s7 drill | 8, 1, 6, 6, 6 | chunks 100, 50, 24, 23, 1: frames per read 4, 2, 1, 1, 0 (total 8), left 6; 50, 50, 50: 6 frames, 6 left | ok; byKey figures match |
| s8 follow-up | spin | no wake-up; epoll still sleeps | ok |
| q-frames | 10 | divmod(250,24) = (10,10); wrong 11 rounds up | ok |
| q-copies | two | kernel path copies twice | ok |
| q-spin | 5000 | 1,000 µs / 0.2; wrong 1000 | ok |
| q-idle | poll | | ok |

### l13-tcp-and-udp

| Item | Key | Computation | Verdict |
|---|---|---|---|
| s0 tap | c4 to c10 | 7 messages after the gap | ok |
| s1 repair | 20000 | 100,000 x 0.2 s; slip 200 (0.002 s) and mid 2000 (20 ms) both reproduce; 0.5 ms gives 50; 200/0.5 = 400 times | ok |
| s2 handshake | 90 | 3 x 30; udp 30, rtt 60 (two trips), four 120 | ok |
| s3 table | 5,000,000, 100,000, 50 | 50 x 1,000 x 100; 40 Mbit/s and 0.8 Mbit/s | ok |
| s4 both lost | 100 | 1,000,000 x 0.0001; one 10,000, sum 20,000, tenth 10; seeds 7 and 8 reproduce "87" in my own run (sd 10.0) | ok |
| s5 UDP sooner | wait | distractors wrong | ok |
| s6 gaps | 1 | [2,1,4,4,5] misses only 3; wrong 2 (late 1 counted) | ok |
| s7 repeat | none | | ok |
| s8 drill | 1, 3, 1, 4 | gaps [3], [2,3,4], [4], [4,5,6,9] | ok; byKey lists match |
| s9 code | solution passes 13 of 13; starter passes 6 of 13 | starter fails [1,3,2], [3,1,2,6,5], [5,4,3,2,1], [2,1,4,3,6], [4,2,3], [1,4,2,3], [3,3,1]; 13 hidden tests as stated | ok |
| s10 NODELAY | nagle | | ok |
| q-handshake | 150 | 3 x 50; wrong 50, 100 | ok |
| q-orders | right | | ok |
| q-gaps | 2 | [1,3]; wrong 3 | ok |
| q-multicast | 2000000 | 10 x 1,000 x 200; wrong 200000 | ok |

### l14-messages-on-the-wire

| Item | Key | Computation | Verdict |
|---|---|---|---|
| s0 tap | c4 to c7 | frame decodes (65, 66, 258, 70000, 123456789, 100, 10275, 36000000); every byKey figure matches; highlight ranges correct | ok |
| s1 little-endian | 258 | `<H` of 02 01 = 258; be 513 | ok |
| s2 table | 10275, 40, 35, 231, 37 | divmod(10275,256) = (40,35); -25 packs to ffffffe7 (e7 = 231); 36,000,000 is 02 25 51 00, 0x25 = 37 | ok |
| s3 table | 4800000, 38.4, 61, 8 | 200,000 x 24; x8/1e6; divmod(1472,24) = (61,8) | ok |
| s4 struct | no | sizeof is 24 (compiled); 70,000 little-endian is 70 11 01 00 | ok |
| s5 edge | -2147483648 | `>i` of 80000000; unsigned 2147483648; ff ff ff ff is 4294967295 and -1 | ok |
| s6 shift | msb | | ok |
| s7 code | solution passes 12 of 12; starter passes 0 of 12 | I rebuilt every expected byte list with `struct.pack`: all 4 encode lists match; the 12 count is right | ok |
| s8 drill | 256, 65536, -200, 120, 125 | 0x100 both ways; ffffff38 is -200; 0x2ee0 = 12,000 pence; 3000/24 | ok |
| s9 flags | 26, 28, 56, 16 | 24 + 2; sizeof 28 (compiled); divmod(1472,26) = (56,16) | ok |
| q-decode | 3000 | 0x0bb8; LE 3,087,728,640 | ok |
| q-negative | 24 | fffffc18, 0x18 = 24; mag 232 | ok |
| q-double | exact | | ok |
| q-frames | 58 | divmod(1400,24) = (58,8); 59 x 24 = 1,416 | ok |

### review-3

| Item | Key | Computation | Verdict |
|---|---|---|---|
| r3-overhead | 153.6 | 6 MiB/8 KiB = 768 x 0.2; wrong 768 | ok, fresh |
| r3-switch | block | | ok |
| r3-chunks | 6, 16 | 50, 50, 60: parses 2, 2, 2; left 16 | ok (see note F4) |
| r3-zero | close | | ok |
| r3-handshake | 60 | 3 x 20; wrong 20, 40 | ok (see note F1) |
| r3-gaps | 3 | max 9, seen {2,3,4,6,8,9}, missing 1, 5, 7; wrong 6 | ok |
| r3-big-endian | 2000 | 0x07d0; LE 3,490,119,680 | ok, fresh |
| r3-neg | 156 | ffffff9c, 0x9c = 156; mag 100 | ok, fresh |
| r3-both-lost | 400 | 1,000,000 x 0.0004; one 20,000, sum 40,000 | ok, fresh |

### homework-3

| Item | Key | Computation | Verdict |
|---|---|---|---|
| h3-two-carriers a | 80 | RTT 80: TCP 120, UDP 40, gap 80 | ok |
| b | 100 | 40,000 x 0.0025; slip 1000 is x10 | ok |
| c | 8000 | 40,000 x 0.2; slip 800; 200/2.5 = 80 times | ok |
| d | 300000 | 2,000 x 150; uni 6,000,000 | ok |
| e | 6000000 | 20 x 300,000; one 300,000 | ok |
| h3-feed-summary | 200, [17,18,90,150,151,152], 31, 10001.412844036697 | my own decode of `feed.hex`: 201 lines of 24 bytes, 200 unique (seq 100 twice, identical), largest 206, 31 trades, VWAP matches to the last digit; starter returns 201, [], 0, 0.0 so fails all four | ok; the dedupe fix is only tested by `unique` and `missing`, since the repeat is not a trade |
| h3-multicast-aloud | rubric 2+2+2+2+1+1 = 10 | 30,000 x 0.2 = 6,000; 100 x 500 x 200 = 10,000,000 vs 100,000, 100 times; 1,000,000 x 0.005 = 5,000; 0.005 squared x 1,000,000 = 25 | ok |
| h3-hand-encode | 12, 44, 99, 232, 251, 0 | packed frame is `54 53 00 0c 00 00 01 2c 00 00 00 63 00 00 03 e8 ff ff ff fb 02 93 2e 00`, as in the explanation; 12 x 3,600,000 = 43,200,000 | ok |
| h3-kernel-budget a | 83333 | 1e6/12 = 83,333.3 (tol 1); rcv 100000 | ok |
| b | 333333 | 1e6/3; rcv 1,000,000 | ok |
| c | 3.6 | 300,000 x 12 µs; two 0.6 is 2 µs only | ok |
| d | 7500 | 300,000/40; all 300000 | ok |
| e | 67.5% | 7,500 x 90 µs = 0.675 s; old 3.6 reads as 360% | ok |
| h3-blocking-recv | s1 to s6, leave out d1 to d3 | all three distractors are wrong as written; `left-out` is a legal byKey | ok (see note F5) |
| h3-save-calls | 499.2 | 5 MiB/2 KiB = 2,560 calls = 512 µs; /80 KiB = 64 calls = 12.8 µs; difference 499.2 | key ok, repeats the lesson (M1) |

## Mismatches

### Wrong keys

None.

### Numbers repeated from a lesson in the same course

1. `homework-3.json`, item `h3-save-calls`: version B makes 64 calls costing 12.8 µs, the same figures as `l11-processes.json` quiz `q-overhead` (64 calls, 12.8 µs, with 64 as its `wrong` value). The homework `wrong` value 12.8 and its explanation repeat them. Fix: use 160 KiB for version B, so B makes 32 calls and costs 6.4 µs. Key 505.6 (512 − 6.4), `wrong` b 6.4 (keep a), `accept` "505.6 µs: 512 µs for version A, 6.4 µs for version B", explanation "B needs 32 calls, 6.4 µs. The saving is 512 − 6.4 = 505.6 µs." Check that 6.4 and 505.6 appear nowhere else.

### Voice: sentences of 20 words (rule is under 20)

2. `l11-processes.json`, screen 3 (`A wake for every message`) prose: "A thread that sleeps on a socket and is woken per message pays two: one to sleep, one to wake." Fix: "A thread woken per message pays two: one to sleep, one to wake."
3. `l11-processes.json`, screen 3 explain: "At 100,000 messages a second that is 0.4 s of every second, 40% of a core, before any real work." Fix: "At 100,000 messages a second that is 0.4 s in every second, or 40% of a core."
4. `l12-files-and-sockets.json`, screen 1 explain: "The kernel path spends 10 µs on two copies and a wake-up: twice the 5 µs budget, before any work." Fix: "The kernel path spends 10 µs on two copies and a wake-up, twice the 5 µs budget."
5. `l12-files-and-sockets.json`, screen 8 prose: "The interviewer asks: blocking `recv`, `epoll` or a busy poll, for a thread with a 5 µs budget per message?" Fix: drop "per message".
6. `l14-messages-on-the-wire.json`, screen 7 explain: "The price is stored as an unsigned 32-bit pattern and cast back to a signed `int`, which restores the sign." Fix: drop "32-bit".

No em-dashes, no exclamation marks, no American spellings, and no explanation over three sentences in the six files.

### Choice key visibly longer than its distractors (key is the longest and at least 1.3 times the mean distractor)

7. `l11-processes.json`, quiz `q-shortcut`: key 41 characters against 28, 14, 23 (ratio 1.89). Lengthen the distractors ("Writing 24 bytes to a socket, which the kernel owns") or shorten the key ("The clock read through the shared page").
8. `l13-tcp-and-udp.json`, screen 7: key 45 against 26, 24 (1.80). Shorten to "Nothing: that number is already held" or lengthen the others.
9. `l12-files-and-sockets.json`, screen 4: key 50 against 39, 30, 37 (1.42).
10. `l12-files-and-sockets.json`, screen 6: key 45 against 33, 38, 25 (1.41).
11. `l12-files-and-sockets.json`, screen 5: key 51 against 35, 42, 37 (1.34).
12. `l12-files-and-sockets.json`, quiz `q-copies`: key 51 against 34, 38, 43 (1.33).
13. `review-3.json`, item `r3-zero`: key 44 against 35, 38, 27 (1.32).

Close but under the line (key longest, ratio 1.22 to 1.29, no action needed): l11 s4, l11 s5, l13 s5, l13 s10, l14 s4, l14 q-double.

### Fresh-number notes (nothing wrong; the fix agent may leave them)

F1. `review-3.json` `r3-handshake`: the key 60 ms equals the round trip (and the `rtt` wrong value) in `l13-tcp-and-udp.json` screen 2. The other numbers differ. Optional: use a 36 ms round trip, key 54, udp 18, rtt 36.
F2. `review-3.json` `r3-gaps`: key 3 equals the key of the l13 drill row "1, 5". The data differ. No action.
F3. `homework-3.json` `h3-kernel-budget`: reuses l12's 10 µs kernel path and 1 µs bypass path as setting constants. All answers are fresh (83,333; 333,333; 3.6; 7,500; 67.5%). No action.
F4. `review-3.json` `r3-chunks`: the first two chunks (50, 50) and the key 6 frames match the l12 drill row "50, 50, 50: 6 frames". Left bytes (16 against 6) and the third chunk differ. Optional: use chunks 60, 50 and 60 (170 bytes: parses 2, 2 and 3 frames, key 7 frames, 2 bytes left).
F5. `homework-3.json` `h3-blocking-recv`: the order task (sleep, packet, wake, copy, return) is close to l12 screen 0, with the card and stack lines removed and a sleep step added. Different lines and distractors. Acceptable.

### Other notes

- In-course repeat between lessons (outside the review and homework rule): `l14-messages-on-the-wire.json` screen 3 repeats the setting of `l11-processes.json` screen 9 (200,000 messages a second, 24 bytes, 1,472 bytes, 61 frames, 8 spare). Optional.
- Consistency: l11 prices a wake at two switches, 4 µs; l12 screen 3 says "the 5 µs wake". Both are round figures in separate contexts. Optional: state in l12 that the 5 µs wake includes both switches and the scheduler, or reuse 4 µs.
- Cross-course grep (other courses, exams, bank, drills): no systems-topic item (datagram, recv, big-endian, multicast, system call) exists outside the `systems` course. Number hits such as 153.6, 2,000 and 400 are in unrelated statistics or finance contexts, and no item there shares two or more numbers with a scope item. No cross-course duplicate.
