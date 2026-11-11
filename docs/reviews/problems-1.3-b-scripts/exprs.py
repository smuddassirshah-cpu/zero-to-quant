"""List every expression part and every set-answer part of the six sets, with wrong[] tex. Run from the repo root."""
import json

for c in ['taylor', 'multivar']:
    for n in (1, 2, 3):
        d = json.load(open(f'app/content/courses/{c}/problems-{n}.json'))
        print(c, n, {k: v for k, v in d.items() if k != 'items'})
        for it in d['items']:
            for i, p in enumerate(it['parts'], 1):
                w = p['widget']
                if w['kind'] == 'expression' or 'answers' in w:
                    print('  ', it['id'], i, json.dumps(
                        {k: v for k, v in w.items() if k not in ('kind', 'keyboard', 'label')}, ensure_ascii=False))
