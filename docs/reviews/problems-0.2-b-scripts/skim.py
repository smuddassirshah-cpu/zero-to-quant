"""One line per screen, quiz item, review item or homework item: the start of its prose and question. For the freshness read.

Usage: python3 docs/reviews/problems-0.2-a-scripts/skim.py <file.json> [width]
"""
import json
import sys

d = json.load(open(sys.argv[1]))
w = int(sys.argv[2]) if len(sys.argv) > 2 else 150


def line(tag, o):
    parts = o.get('parts') or []
    q = o.get('question') or ' | '.join((p.get('question') or '')[:w // 2] for p in parts)
    print(f"{tag} [{o.get('type', '')}] {(o.get('prose') or '')[:w]} ## {q[:w]}".replace('\n', ' '))


for key in ('screens', 'quiz', 'items'):
    for i, o in enumerate(d.get(key, [])):
        line(f'{key}[{i}]', o)
