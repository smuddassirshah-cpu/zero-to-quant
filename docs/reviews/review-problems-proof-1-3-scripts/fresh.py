"""Second read, proof problems-1 to -3: where each problem's figures, formulas and story nouns occur in app/content
(the three sets themselves left out), and the same for the nouns and claims of the proposed fixes.
The reuse findings come from reading the course beside the sets (taught.py, peek.py); this only helps.
Usage (repo root): python3 docs/reviews/review-problems-proof-1-3-scripts/fresh.py [--all]   (--all lists files outside the course too)"""
import glob
import re
import sys

ALL = '--all' in sys.argv
OWN = {f'app/content/courses/proof/problems-{n}.json' for n in (1, 2, 3)}
files = [f for f in glob.glob('app/content/**/*.json', recursive=True) if f not in OWN and not f.endswith('manifest.json')]
text = {f: open(f).read() for f in files}
PAT = {
    'p-leverage-calls': [r'margin call', r'margin rule', r"broker's rule", r'leverage', r'\b40 (client )?accounts', r'\b9 (are|pass|trade)? ?(in )?both', r'A book holds 40'],
    'p-spread-signal': [r'20-day average', r'volume (is|was) above \d', r'P \\\\lor Q\) \\\\land \\\\lnot R', r'8\.40', r'8\.25', r'spread (is )?wider', r'spread widens'],
    'p-fund-thresholds': [r'[Cc]laim A', r'[Cc]laim B', r'every trader made more than', r'there is a (day|week|year) (on|in) which every', r'annual returns'],
    'p-multiples-forty': [r'\\\\dots, 40\\\\}', r'multiples of 4', r'multiples of 6', r'U = \\\\\{1, (2, )?\\\\dots, \d+\\\\\}'],
    'p-jobs-servers': [r'\b1296\b', r'\b936\b', r'servers', r'How many functions', r'one-to-one functions are there', r'to one of \d+ (servers|venues|projects|brokers)'],
    'p-rule-and-domain': [r'9 - 3x', r'Which opening starts a proof that \$f\$ is one-to-one', r'Which \$x\$ has \$f\(x\) = y\$\? Write it in terms of \$y\$', r'f\^\{-1\}\(-\d+\)'],
    'p-shift-images': [r'two to a desk', r'share a desk', r'f\(A \\\\cap B\)', r'traders? .{0,40}desks?', r'early shift'],
    'p-two-odd-squares': [r'm\^2 \+ n\^2', r'a\^2 \+ b\^2', r'j\^2 \+ j', r'sum of two squares', r'What goes in the bracket'],
    'p-step-three-sum': [r'1 \+ 4 \+ 7', r'3n - 2', r'4n - 3', r'\b2380\b', r'\\\\dfrac\{\(k \+ 1\)\(\\\\ \\\\square\\\\ \)\}\{2\}'],
    'p-six-nine-lots': [r'6x \+ 9y', r'no integers', r'remainder does 100', r'opens a proof'],
    'p-even-test-contra': [r'n\^2 \+ 6n \+ 1', r'n\^2 - 6n \+ 5', r'Which statement should we prove instead', r'2k\^2 [+-] 6k', r'Clearly'],
    'proposed fixes': [r'parcel', r'heavy label', r'\bkiln', r'\bglaz', r'\bberth', r'\bquay', r'ferr(y|ies)', r'n\^2 \+ 2\b', r'remainder 1 on division by 3', r'3jk', r'9k\^2 \+ 2'],
}
for item, pats in PAT.items():
    print(f'== {item}')
    for p in pats:
        hits = sorted(f for f, t in text.items() if re.search(p, t))
        own = [h.split('/')[-1][:-5] for h in hits if '/courses/proof/' in h]
        ex = [h.split('/')[-1][:-5] for h in hits if h.endswith(('exams/topic-0.6.json', 'exams/stage-0.json'))]
        other = [h for h in hits if '/courses/proof/' not in h and not h.endswith(('exams/topic-0.6.json', 'exams/stage-0.json'))]
        line = f'  {p!r}: course {own or 0}; its exams {ex or 0}; elsewhere {len(other)}'
        if ALL and other:
            line += ' ' + ', '.join(o.replace('app/content/', '') for o in other[:12])
        print(line)
