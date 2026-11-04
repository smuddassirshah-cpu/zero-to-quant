s = open('b19.py').read()
reps = [
    ("'ladder', 2, 'Two at once', L3,", "'trap', 2, 'Two at once', L3,"),
    ("{'all': \"You accepted `[2, 5)`, but at time 3 two bookings already stand.\",",
     "{'all': \"You checked only the start of `[2, 5)`. At time 3, inside it, two bookings already stand.\","),
    ('"Check runs 8 hidden tests: three from stage A with one booking at a time, and five with `k` up to 3."',
     '"Check runs 8 hidden tests. Three repeat stage A, and five use `k` up to 3."'),
    ("A sorted map of +1 and -1 changes finds a start in $O(\\\\log n)$ but must still walk the changes inside the new interval. Say the cost and the trade-off aloud.",
     "A sorted map of +1 and -1 changes finds a start in $O(\\\\log n)$, but it walks the changes inside the new interval. Say the cost and the trade-off aloud."),
    ('"A live round is reported to run in layers: clarify, base, test, then follow-ups that change a rule or add an operation."',
     '"A live round is reported to run in layers. Clarify, base and test come first, then follow-ups that change a rule or add an operation."'),
    ('"A tree that adds on a range and keeps the maximum per part does this in $O(\\\\log n)$."),',
     '"A tree that adds on a range and keeps the maximum per part does this in $O(\\\\log n)$.", ["l1", "l3"]),'),
]
for a, b in reps:
    if a not in s:
        print('MISSING', a[:60])
        continue
    s = s.replace(a, b)
open('b19.py', 'w').write(s)
