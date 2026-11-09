"""Freshness grep: for each drill, look for the same task under another story in the taught courses
(lessons, reviews, homework) of ds, algo-think, graphs-dp, coding-int and contests, and in other drills.
Usage: fresh_grep.py <app/content> [drill ids...]. Prints each hit with a short snippet; the judging is in the review."""
import glob, json, os, re, sys
ROOT = sys.argv[1]
PAT = {
    'dsa-route-order': r'no pair points|itinerary|reconstruct the (route|chain|list)',
    'dsa-shallowest-leaf': r'min(imum)?[ _-]depth|nearest leaf|shallowest|shortest path from the root',
    'dsa-shared-tail': r'intersect\w* (of )?(two )?(linked )?lists|merge point|share (a|their) tail|where two (lists|queues)',
    'dsa-common-manager': r'common ancestor|lowest common|\blca\b',
    'dsa-closest-level': r'closest value|nearest (value|level|key)|floor and ceiling|in-order predecessor',
    'dsa-swapped-levels': r'swapped|recover (the )?(tree|bst)',
    'dsa-nearest-strikes': r'k closest|closest k|nearest k|k nearest',
    'dsa-short-codes': r'unique prefix|shortest prefix|prefix that (starts|identif)',
    'dsa-print-queue': r'shortest job|fewest pages|single.threaded|printer',
    'dsa-window-every-venue': r'smallest range|one (value|element|number|time) from (each|every)|covering .* lists',
    'dsa-total-booked': r'total (covered )?length|covered length|union of (the )?intervals|minutes .* (booked|covered)',
    'dsa-double-booked': r'can_attend|attend (all|every)|any (two )?(overlap|clash)',
    'dsa-peak-calls': r'meeting rooms|rooms needed|max(imum)? (number of )?(overlap|concurrent)|most .* at (once|the same)',
    'dsa-cover-opening': r'video stitch|fewest (intervals|shifts|clips)|minimum number of (taps|intervals|clips)|cover the (whole|full) (range|day|interval)',
    'dsa-shortest-cover': r'smallest interval|shortest (interval|window) (that )?(covers|containing)|for each query.*interval',
    'dsa-lift-buttons': r'elevator|\blift\b|button',
    'dsa-spare-cables': r'cable|make .* connected|redundant (edge|connection)',
    'dsa-climb-limit': r'climb|height difference|heights\[',
    'dsa-upstream-stations': r'revers\w* (every |the |each )?(edge|pipe|arrow)|transpose|can reach (the )?(target|reservoir|node)',
    'dsa-forced-order': r'unique topolog|only one (valid )?order|exactly one (valid )?order|hamiltonian',
    'dsa-footpath-slabs': r'tiling|tiles?\b|domino|2 ?(by|x|\\times) ?n|paving|slab',
    'dsa-stamp-gaps': r'stamp|cannot be made|unmakeable|frobenius|coin problem',
    'dsa-shift-pay': r'three (days )?in a row|three consecutive|house robber|no two (adjacent|neighbouring|days in a row)',
    'dsa-feed-passes': r'\bpass(es)?\b.*(7|seven)|7-day|30-day|travel ticket',
    'dsa-free-desk-square': r'largest square|maximal square|biggest square',
    'dsa-kiosk-change': r'lemonade|exact change|£5 note|give change',
    'dsa-loop-depots': r'gas station|petrol|fuel|circuit',
    'dsa-ticker-batches': r'partition labels|last (occurrence|appearance)|as many (parts|pieces|batches)',
    'dsa-split-prices': r'ip address|restore|separators? (were |was )?lost|split .* digits',
    'dsa-server-loads': r'k (workers|servers|machines)|makespan|minimum time to finish|busiest (server|worker)|k equal(-sum)? subsets|partition into k',
    'dsa-oncall-rota': r'(count|number of) (sub)?(arrays|runs|windows|substrings) (with|of) (all )?distinct|no repeat',
    'dsa-depth-block': r'sum of (the )?(subarray )?min|sum over every (block|subarray|window)|subarray minim',
    'dsa-range-volumes': r'rises? |beat the (bar|day) before|more than the (bar|day) before',
}
files = []
for c in ('ds', 'algo-think', 'graphs-dp', 'coding-int', 'contests'):
    files += sorted(glob.glob(os.path.join(ROOT, 'courses', c, '*.json')))
files += sorted(glob.glob(os.path.join(ROOT, 'drills', '*.json')))
texts = {f: open(f).read() for f in files}
ids = sys.argv[2:] or sorted(PAT)
for i in ids:
    rx = re.compile(PAT[i], re.I)
    hits = []
    for f, t in texts.items():
        if os.path.basename(f) == i + '.json' or f.endswith('index.json'):
            continue
        ms = list(rx.finditer(t))
        if ms:
            m = ms[0]
            hits.append('%s x%d: ...%s...' % (os.path.relpath(f, ROOT), len(ms), t[max(0, m.start() - 60):m.end() + 60].replace('\\n', ' ').replace('\n', ' ')))
    print('==', i, len(hits), 'files')
    for h in hits[:8]:
        print('   ', h)
