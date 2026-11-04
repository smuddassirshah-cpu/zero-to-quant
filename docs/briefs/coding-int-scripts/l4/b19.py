from lib2 import *
import refs4 as R

L1 = ['live-round']
L2 = ['calendar-booking']
L3 = ['follow-up-layering']


def nl(intervals, mx=10, tap=False, caption=None):
    ivs = []
    for i, (a, b) in enumerate(intervals):
        ivs.append({"id": f"i{i + 1}", "from": a, "to": b, "row": i + 1, "label": f"[{a}, {b})", "labelPos": "right", "open": [False, True]})
    st = {"intervals": ivs}
    if caption:
        st["caption"] = caption
    p = {"min": 0, "max": mx, "step": 1, "labels": 1}
    if tap:
        p["tapIntervals"] = True
    return {"kind": "number-line", "params": p, "state": st}


def a_tests():
    t = [{'call': f"run_cal({k}, {ops!r})", 'expect': e} for k, ops, e in R.CAL_A[:3]]
    t += [{'call': f"run_cal({k}, {ops!r})", 'expect': e} for k, ops, e in R.CAL_A[3:]]
    t.append({'setup': 'ops = [[0, 2 * i, 2 * i + 1] for i in range(60000)] + [[0, 0, 120000]]', 'call': 'run_cal(1, ops).count(True)', 'expect': 60000})
    return t


def b_tests():
    t = [{'call': f"run_cal({k}, {ops!r})", 'expect': e} for k, ops, e in R.CAL_A[:3]]
    t += [{'call': f"run_cal({k}, {ops!r})", 'expect': e} for k, ops, e in R.CAL_B]
    return t


def c_tests():
    t = b_tests()
    t += [{'call': f"run_cal({k}, {ops!r})", 'expect': e} for k, ops, e in R.CAL_C]
    return t


def stmt(lines, title='Calendar'):
    return console(title, lines)


def lesson():
    S = []
    # 1 hook tap
    S.append(screen(
        'problem', 1, 'Which bookings are accepted', L1,
        "A calendar takes a booking `[start, end)`: the start counts, the end does not. A booking is accepted if it overlaps none already accepted. "
        "You merged intervals in l1-merging-intervals. New here: a live round that adds rules part-way.",
        "Bookings arrive in the order shown, with one booking allowed at a time. Tap the ones that are accepted.",
        {"kind": "tap-regions", "answer": ["i1", "i3", "i4"], "countWord": "bookings",
         "wrong": [{"id": "all", "set": ["i1", "i2", "i3", "i4"]}]},
        hints("Take the bookings one at a time, in order.",
              "The second, `[3, 6)`, starts inside `[1, 4)`.", "`[4, 8)` starts exactly where `[1, 4)` ends, and the end does not count. `[0, 1)` also touches without overlap.", ["i2"]),
        fb("`[1, 4)`, `[4, 8)` and `[0, 1)` are accepted. `[3, 6)` overlaps the first.", "Not quite right. A booking is refused only if it shares a time with one already accepted.",
           {'all': "You accepted every booking. `[3, 6)` overlaps `[1, 4)` between 3 and 4.", 'i2': "`[3, 6)` shares the times 3 with `[1, 4)`, which was accepted first.",
            'i3': "`[4, 8)` starts at 4, and `[1, 4)` does not include 4, so they do not overlap.", 'i4': "`[0, 1)` ends at 1, and `[1, 4)` starts at 1, so they do not overlap.",
            'i1': "The first booking meets an empty calendar, so it is accepted."}),
        explain("`[3, 6)` shares the time 3 with `[1, 4)`, so it is refused. `[4, 8)` and `[0, 1)` only touch it, because the end is not included. Three bookings are accepted."),
        canvas=nl([(1, 4), (3, 6), (4, 8), (0, 1)], mx=9), pace=90))
    # 2 clarify
    S.append(screen(
        'ladder', 1, 'The first five minutes', L1,
        "A live round of 45 minutes is reported to open with five minutes of questions. Choose the one that matters most to the examples.",
        "Which question changes whether `[1, 4)` and `[4, 8)` clash?",
        choice([
            ('a', 'Is the end of a booking included?', None),
            ('b', 'Can a booking be cancelled later?', "You chose a question for a later stage. It does not change whether these two clash."),
            ('c', 'Which language should I use?', "You asked about tools. The ends of a booking decide the examples."),
            ('d', 'How many bookings will there be?', "You asked about size. It changes the speed you need, not the answers."),
        ]),
        hints("Look at where the two bookings meet.",
              "They meet at the time 4.", "If the end is included, both hold 4 and clash. If it is not, they do not.", ["i1", "i3"]),
        fb("The end rule decides the examples, so ask it first.", "Not quite right. Which question changes an answer you can see?",
           {'b': "Cancelling matters for stage C, not for this clash.", 'c': "The language does not change which bookings clash.", 'd': "The count changes the design, not the answers to these examples."}),
        explain("The two bookings meet at 4. Whether they clash depends on whether the end counts. Ask it first, then whole numbers, then cancellation."),
        canvas=nl([(1, 4), (4, 8)], mx=9), pace=60))
    # 3 stage A
    ex = [{'call': 'run_cal(1, [[0, 10, 20], [0, 15, 25], [0, 20, 30]])', 'expect': [True, False, True]}, {'call': 'run_cal(1, [[0, 5, 10], [0, 0, 5]])', 'expect': [True, True]}]
    cw = code('python', R.CAL_STARTER, R.CAL_A_SOL, ex, a_tests(),
              "Check runs 6 hidden tests, from the edge of a booking to 60,000 bookings. The driver `run_cal` is hidden.", postlude=R.CAL_DRIVER_A)
    S.append(screen(
        'problem', 3, 'Stage A: book', L2,
        "Write `Calendar()` with `book(start, end)`. Keep the starts and ends sorted, and use `bisect` to find the place. The starter accepts everything.",
        "Write `Calendar` and `book`.",
        cw,
        hints("Which two bookings can overlap a new one?",
              "Only its neighbours in the sorted order.", "The one before must end by `start`. The one after must start at or after `end`. Use `bisect_left` on the starts.", ["l1", "l2"]),
        fb("Check the left neighbour's end and the right neighbour's start.", "Not quite right. Check the first failing test.",
           tkeys(6, {1: "Test 1: `[20, 30)` touches `[10, 20)` and is accepted.", 2: "Test 2: bookings that touch at an end are accepted.", 3: "Test 3: bookings that fit around each other are accepted.",
                     6: "Test 6 has 60,000 bookings. Scanning every booking each time is too slow."})),
        explain("Because accepted bookings never overlap, the sorted order is also the time order. A new booking can clash only with the one before or after its place. Two comparisons settle it."),
        canvas=stmt(["Calendar().book(start, end)", "Accept a booking [start, end) if it overlaps none accepted.", "Return True if accepted, False if not.",
                     "The driver run_cal(k, ops) is hidden: rows [0, start, end] book."]), pace=900))
    # 4 numeric
    S.append(screen(
        'ladder', 2, 'Run stage A by hand', L2,
        "Run stage A on five bookings, with one allowed at a time: `[2, 5)`, `[5, 7)`, `[4, 6)`, `[7, 9)` and `[0, 2)`.",
        "How many are accepted?",
        numeric(4, 'Accepted', '4: all but `[4, 6)`', [('all', 5), ('three', 3)]),
        hints("Which booking overlaps an earlier one?",
              "`[4, 6)` starts inside `[2, 5)` and also inside `[5, 7)`.", "The other four only touch at an end, so they are accepted.", ["i3"]),
        fb("`[4, 6)` is refused. The other four are accepted.", "Not quite right. Compare each booking with the accepted ones.",
           {'all': "You accepted `[4, 6)`, but it overlaps `[2, 5)` between 4 and 5.", 'three': "You refused one booking too many. The others only touch at an end."}),
        explain("`[2, 5)` and `[5, 7)` touch, so both are accepted. `[4, 6)` overlaps both and is refused. `[7, 9)` and `[0, 2)` only touch, so four are accepted."),
        canvas=nl([(2, 5), (5, 7), (4, 6), (7, 9), (0, 2)], mx=10), pace=60))
    # 5 stage B
    cw = code('python', R.CAL_B_STARTER, R.CAL_BC_SOL, ex, b_tests(),
              "Check runs 8 hidden tests. Three repeat stage A, and five use `k` up to 3.", postlude=R.CAL_DRIVER)
    S.append(screen(
        'problem', 3, 'Stage B: up to k at once', L3,
        "First follow-up: `Calendar(k)` allows up to `k` bookings at any instant. The sorted-list shortcut breaks, because neighbours no longer decide. "
        "Complete `_fits`: count the overlaps at the new start and at each booking start inside the new interval.",
        "Complete `_fits` so `book` honours `k`.",
        cw,
        hints("Where can the number of overlaps rise inside the new interval?",
              "Only at a time where another booking starts.", "Check the new start, and every booking start strictly inside the new interval. At each, count bookings with `s <= p < e`.", ["l1", "l2"]),
        fb("Check the start and each booking start inside.", "Not quite right. Check the first failing test.",
           tkeys(8, {4: "Test 4: with `k = 2`, a booking inside two others at time 15 is refused.", 5: "Test 5: with `k = 2`, `[5, 11)` meets two bookings at time 10.",
                     6: "Test 6: with `k = 3`, the fourth booking overlaps three at time 4.", 8: "Test 8: with `k = 2`, `[5, 15)` meets two bookings at time 5."})),
        explain("The overlap count changes only where a booking starts. So it is enough to test the new start and every start inside the new interval. If none exceeds `k - 1`, the booking fits."),
        canvas=stmt(["Calendar(k).book(start, end)", "At most k bookings may cover any instant.", "_fits(start, end) checks the new start",
                     "and each booking start inside the new interval."]), pace=900))
    # 6 numeric
    S.append(screen(
        'trap', 2, 'Two at once', L3,
        "With `k = 2`, bookings arrive in the order `[1, 4)`, `[3, 6)`, `[2, 5)` and `[4, 8)`.",
        "How many are accepted?",
        numeric(3, 'Accepted', '3: all but `[2, 5)`', [('all', 4), ('two', 2)]),
        hints("Look at the time 3.",
              "At time 3, `[1, 4)` and `[3, 6)` are both booked.", "`[2, 5)` would be a third at time 3, so it is refused. `[4, 8)` starts when `[1, 4)` has ended.", ["i3"]),
        fb("`[2, 5)` is refused: at time 3 it would be the third booking.", "Not quite right. Count the bookings at each start inside the new one.",
           {'all': "You checked only the start of `[2, 5)`. At time 3, inside it, two bookings already stand.", 'two': "You refused `[4, 8)` too. At 4, `[1, 4)` has ended, so only `[3, 6)` stands."}),
        explain("`[1, 4)` and `[3, 6)` both fit, as two may overlap. `[2, 5)` would make three at time 3, so it is refused. `[4, 8)` meets only `[3, 6)`, so three are accepted."),
        canvas=nl([(1, 4), (3, 6), (2, 5), (4, 8)], mx=9), pace=60))
    # 7 stage C
    cw = code('python', R.CAL_C_STARTER, R.CAL_BC_SOL, ex, c_tests(),
              "Check runs 13 hidden tests: stages A and B again, then `cancel` and `next_free`.", postlude=R.CAL_DRIVER)
    S.append(screen(
        'problem', 3, 'Stage C: cancel and next_free', L3,
        "Second follow-up: `cancel(start, end)` removes one exact earlier booking. `next_free(duration, after)` returns the earliest whole start at or after `after` where a booking of that length would be accepted. "
        "The candidates are `after` and the end of each booking after it.",
        "Add `cancel` and `next_free`.",
        cw,
        hints("Where can the earliest free start be?",
              "At `after`, or just when some booking ends.", "Try `after` and each booking end above it, in order, with `_fits`. Return the first that fits.", ["l1", "l2"]),
        fb("Try `after` and each later end, in order.", "Not quite right. Check the first failing test.",
           tkeys(13, {9: "Test 9: `cancel` must report False when there is no exact match, and remove only one booking.", 10: "Test 10: a free start is the first candidate where the booking fits.",
                      11: "Test 11: after the cancel, the freed time is available again.", 12: "Test 12: an empty calendar gives `after` itself.", 13: "Test 13: cancelling frees the gap that `next_free` then finds."})),
        explain("A free start only improves when a booking ends, so the candidates are `after` and the ends above it. We test them in order with the same `_fits` check. `cancel` removes the exact pair and nothing else."),
        canvas=stmt(["Calendar(k).cancel(start, end)", "Remove one exact earlier booking. Return True if it was there.", "next_free(duration, after)",
                     "The earliest whole start at or after `after` where a booking that long is accepted."]), pace=900))
    # 8 numeric
    S.append(screen(
        'ladder', 3, 'Cancel and look again', L3,
        "With `k = 1`: book `[9, 12)`, book `[12, 15)`, ask `next_free(3, 9)`, ask `next_free(2, 9)`, cancel `[9, 12)`, then ask `next_free(3, 9)` once more.",
        "What does the last `next_free(3, 9)` return?",
        numeric(9, 'Start', '9: the cancel freed the time from 9 to 12', [('before', 15), ('twelve', 12)]),
        hints("What does the cancel change?",
              "It frees 9 to 12.", "A booking of 3 starting at 9 now fits exactly before `[12, 15)`.", ["i1", "i2"]),
        fb("After the cancel, `[9, 12)` is free and `next_free(3, 9)` is 9.", "Not quite right. The cancel removes a booking.",
           {'before': "That is the answer before the cancel. After it, the time 9 is free.", 'twelve': "A booking of 3 at 12 would overlap `[12, 15)`. The free start is 9."}),
        explain("Before the cancel, both bookings fill 9 to 15, so the first free start for 3 is 15. The cancel frees 9 to 12. A booking of 3 then fits at 9."),
        canvas=nl([(9, 12), (12, 15)], mx=16, caption="Before the cancel: next_free(3, 9) is 15"), pace=90))
    # 9 E8
    S.append(screen(
        'transfer', 3, 'Sit a round', L1,
        "Open `#drill`, set the pattern to `intervals` and the difficulty to 4, and pick one drill in Python or C++. "
        "The stopwatch counts up from the moment it opens, so keep the 45-minute plan.",
        "Which plan fits a 45-minute round with two follow-ups?",
        choice([
            ('a', 'Clarify 5, base 10, test 5, first follow-up 10, second follow-up 10, explain 5', None),
            ('b', 'Clarify 0, base 25, test 0, first follow-up 10, second follow-up 10, explain 0', "You skipped the clarifying, the tests and the explaining. A wrong reading then costs the whole base."),
            ('c', 'Clarify 15, base 15, test 5, follow-ups 5 and 5, explain 0', "You spent a third of the round on questions. The follow-ups then get 5 minutes each."),
            ('d', 'Clarify 5, base 30, test 5, first follow-up 5, second follow-up 0, explain 0', "You gave the base most of the time. The second follow-up is never reached."),
        ]),
        hints("The plan has six blocks that add to 45.",
              "5, 10, 5, 10, 10 and 5.", "Check that the blocks add to 45 and that every follow-up has 10 minutes.", ["l4", "l5"]),
        fb("5, 10, 5, 10, 10 and 5 add to 45 and leave 10 minutes for each follow-up.", "Not quite right. Add the blocks and compare them with the follow-ups.",
           {'b': "Zero minutes to clarify, test or explain gives up the marks those blocks earn.", 'c': "Questions that long leave only 5 minutes for each follow-up.", 'd': "A base of 30 minutes starves both follow-ups."}),
        explain("Six blocks fill 45 minutes: 5, 10, 5, 10, 10 and 5. The tests come before the follow-ups, and the explanation comes last. After the drill, compare your stopwatch with these blocks."),
        canvas=console('A 45-minute round', ["Clarify and give examples.", "Write the base.", "Test it.", "First follow-up.", "Second follow-up.", "Explain the trade-offs."]), pace=120))
    # 10 generalise order
    S.append(screen(
        'generalise', 2, 'The 45-minute plan', L1,
        "A live round has layers. Each layer extends the code you already have.\n\n"
        "```python\n# 00 clarify, examples        (5)\n# 05 base: book              (10)\n# 15 test                    (5)\n"
        "# 20 follow-up 1: k          (10)\n# 30 follow-up 2: cancel     (10)\n# 40 explain the trade-offs   (5)\n```",
        "Put the 45-minute plan in order.",
        order([
            ('p1', 'Clarify the rules and write examples', None),
            ('p2', 'Write the base problem', None),
            ('p3', 'Test the base against the examples', None),
            ('p4', 'Add the first follow-up', None),
            ('p5', 'Add the second follow-up', None),
            ('p6', 'Explain the design and what you would change at scale', None),
        ], ['p1', 'p2', 'p3', 'p4', 'p5', 'p6']),
        hints("What must be settled before any code?",
              "The rules and some examples.", "Clarify, base, test, follow-up 1, follow-up 2, explain."),
        fb("Clarify, base, test, two follow-ups, explain.", "Not quite right. Each layer builds on a tested one.",
           {'p3': "Test the base before you extend it.", 'p6': "The explanation comes last."}),
        explain("The base is tested before the first follow-up, so a failure points at the new layer. The explanation of trade-offs closes the round."),
        canvas=console('A 45-minute round', ["Clarify and give examples.", "Write the base.", "Test it.", "First follow-up.", "Second follow-up.", "Explain the trade-offs."]), pace=90))
    # 11 transfer choice scale
    S.append(screen(
        'transfer', 3, 'Ten million bookings', L2,
        "The interviewer asks for 10 million bookings, general `k`, and a cost of $O(\\log n)$ per booking. The scan costs $O(n)$ and a sorted list pays to shift entries.",
        "Which structure meets the cost?",
        choice([
            ('a', 'A tree over the times that keeps the largest overlap per part: $O(\\log n)$', None),
            ('b', 'A hash map of bookings by start: $O(1)$ lookups', "You chose a map with no order. It cannot tell the overlap at a time without a scan."),
            ('c', 'A heap of end times: $O(\\log n)$ per push', "You chose the earliest end only. A heap cannot count the bookings at an arbitrary time."),
            ('d', 'The same list, scanned faster in a lower-level language', "You kept the scan. A faster scan is still $O(n)$ per booking."),
        ]),
        hints("What must the structure answer about a time range?",
              "The largest number of overlaps inside it.", "A tree that adds on a range and keeps the maximum per part does this in $O(\\log n)$.", ["l1", "l3"]),
        fb("A tree with a range maximum answers 'does it fit?' in $O(\\log n)$.", "Not quite right. The structure must find the largest overlap in a range.",
           {'b': "A hash map has no order, so a range query needs a scan.", 'c': "A heap gives the earliest end, not the overlap at a time.", 'd': "Speeding up a scan does not change its cost per booking."}),
        explain("A balanced or segment tree keeps the largest overlap per part of the time line. A sorted map of +1 and -1 changes finds the start in $O(\\log n)$ but walks the changes inside. Say the cost and the trade-off aloud.")
        , canvas=console('Scaling up', ["10 million bookings.", "General k.", "Target: O(log n) per booking."]), pace=120))

    quiz = [
        item('q-half', 2, None, L2, "With one booking allowed at a time, `[2, 6)` is accepted. Is `[6, 9)` accepted next?",
             choice([('a', 'Yes: the end 6 is not included, so they only touch', None),
                     ('b', 'No: both contain the time 6', "You counted the end as included. In `[2, 6)` the last time is 5."),
                     ('c', 'No: bookings may not touch', "You made touching illegal. Touching is allowed when the end is excluded."),
                     ('d', 'Yes, but only if you cancel the first', "You thought the first must go. They do not overlap.")]),
             fb("`[2, 6)` holds 2 to 5, and `[6, 9)` starts at 6, so they do not overlap.", "Not quite right. List the whole times of each booking.",
                {'b': "The first booking holds 2, 3, 4 and 5.", 'c': "Touching bookings do not share a time.", 'd': "No cancel is needed."}),
             explain("A half-open booking `[2, 6)` holds the times 2 to 5. `[6, 9)` starts at 6, so the two share nothing."), quiz=True),
        item('q-k', 3, None, L3, "With `k = 2`, `[0, 5)` and `[3, 8)` are booked. Is a new `[4, 6)` accepted?",
             choice([('a', 'No: at time 4 two bookings already stand', None),
                     ('b', 'Yes: it overlaps only one at a time', "You counted one overlap. At time 4, both `[0, 5)` and `[3, 8)` are booked."),
                     ('c', 'Yes: `k` is 2, so any booking is accepted', "You read `k` as a count of bookings. It limits the overlap at one time."),
                     ('d', 'No: `[4, 6)` is shorter than the others', "You compared lengths. Only the overlap counts.")]),
             fb("At time 4 two bookings stand, so a third would break `k = 2`.", "Not quite right. Count the bookings at the new start.",
                {'b': "At 4 both earlier bookings are active.", 'c': "`k` limits how many overlap at one time.", 'd': "The length does not matter."}),
             explain("At time 4 the bookings `[0, 5)` and `[3, 8)` both stand. A new booking would be the third, so it is refused."), quiz=True),
        item('q-free', 3, None, L3, "With `k = 1`, `[4, 7)` and `[7, 9)` are booked. What does `next_free(2, 5)` return?",
             numeric(9, 'Start', '9: after both bookings', [('five', 5), ('seven', 7)]),
             fb("A booking of 2 at 9 fits after `[7, 9)`.", "Not quite right. Try the candidates `after` and each later end.",
                {'five': "A booking at 5 overlaps `[4, 7)`.", 'seven': "A booking at 7 overlaps `[7, 9)`."}),
             explain("The candidates are 5, 7 and 9. At 5 the booking overlaps `[4, 7)` and at 7 it overlaps `[7, 9)`. At 9 it fits."), quiz=True),
        item('q-plan', 2, None, L1, "A 30-minute round has one follow-up. Which plan fits: clarify, base, test, follow-up, explain?",
             choice([('a', '3, 10, 3, 10, 4', None),
                     ('b', '0, 15, 0, 15, 0', "You dropped the clarifying, the tests and the explaining."),
                     ('c', '10, 5, 5, 5, 5', "You spent a third of the round on questions. The base then has 5 minutes."),
                     ('d', '3, 10, 3, 10, 10', "These add to 36, six more than the round has.")]),
             fb("3, 10, 3, 10 and 4 add to 30 and keep every block.", "Not quite right. Check that the blocks add to 30 and none is zero.",
                {'b': "Zero blocks lose the marks those blocks earn.", 'c': "Ten minutes of questions starve the base.", 'd': "36 minutes do not fit in a 30-minute round."}),
             explain("The blocks must add to 30 and each must be present. Only 3, 10, 3, 10 and 4 do both."), quiz=True),
    ]
    return {
        "id": "l19-a-live-round", "course": "coding-int", "title": "A live coding round", "minutes": 15,
        "objectives": ["Work a 45-minute live problem with two follow-ups."],
        "skills": ["ci-timed", "ci-design"], "screens": S,
        "summary": summary(
            ["A live round is reported to run in layers. Clarify, base and test come first, then follow-ups that change a rule or add an operation.",
             "A half-open booking holds its start but not its end. With `k` above 1, test the new start and every booking start inside it.",
             "Keep the 45-minute plan: 5, 10, 5, 10, 10 and 5. Say the cost and the trade-offs of each design aloud."],
            "The plan", "5 + 10 + 5 + 10 + 10 + 5 = 45",
            "Clarify, base, test, follow-up 1, follow-up 2, explain.",
            "Starting the follow-up before the base is tested."),
        "quiz": quiz,
    }
