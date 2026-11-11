"""Skim a lesson, review, homework or exam file: title, prose and question of each screen or item, cut to N characters.
   skim.py <N> <file> [<file> ...]"""
import json
import sys

N = int(sys.argv[1])


def cut(s):
    s = ' '.join(str(s or '').split())
    return s if len(s) <= N else s[:N] + '...'


for f in sys.argv[2:]:
    d = json.load(open(f))
    print('#' * 8, f.split('/')[-1], '|', d.get('title', ''), '|', '; '.join(d.get('objectives', []))[:400])
    for key in ('screens', 'quiz', 'items'):
        for i, s in enumerate(d.get(key) or [], 1):
            if not isinstance(s, dict):
                continue
            print(f'{key[0]}{i} [{s.get("type", s.get("id", ""))}] {s.get("title", "")}: {cut(s.get("prose"))} Q: {cut(s.get("question"))}')
            for j, p in enumerate(s.get('parts') or [], 1):
                print(f'     part {j}: {cut(p.get("question") or p.get("prose"))}')
    if d.get('summary'):
        print('SUMMARY:', cut(json.dumps(d['summary'], ensure_ascii=False))[:1200])
