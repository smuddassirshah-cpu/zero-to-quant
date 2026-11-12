"""Compare each finance and coding item's fields with its row in section 5 of docs/briefs/bank-2.md:
family, difficulty, kind, pace, roles, the Draws-on lesson (requires at difficulty 4 and 5; its skills otherwise).
Prints differences only. With an item id as argument, prints that row of the brief."""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.join(HERE, '..', '..', '..')
rows = {}
for line in open(os.path.join(REPO, 'docs', 'briefs', 'bank-2.md')):
    if line.startswith('| `'):
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        rows[cells[0].strip('`')] = cells
if len(sys.argv) > 1:
    for a in sys.argv[1:]:
        print(a, '::', ' | '.join(rows.get(a, ['no row'])[1:])[:1500], '\n')
    sys.exit(0)
ROLE = {'T': 'trader', 'R': 'research', 'S': 'strats', 'D': 'developer'}
n = miss = 0
for fam in ('finance', 'coding'):
    for k in (1, 2, 3, 4):
        for it in json.load(open(os.path.join(REPO, 'app', 'content', 'bank', f'{fam}-{k}.json')))['items']:
            n += 1
            r = rows.get(it['id'])
            if not r:
                miss += 1
                print('no brief row:', it['id'])
                continue
            family, d, kind, pace, roles, draws = r[1].strip('`'), r[2], r[3], r[4], r[5], r[6].strip('`')
            diffs = []
            if family != it['tags'][0]:
                diffs.append(f'family {family} -> {it["tags"][0]}')
            if str(it['difficulty']) != d:
                diffs.append(f'difficulty {d} -> {it["difficulty"]}')
            if kind.split()[0] != it['widget']['kind']:
                diffs.append(f'kind {kind} -> {it["widget"]["kind"]}')
            if str(it.get('pace')) != pace:
                diffs.append(f'pace {pace} -> {it.get("pace")}')
            want = sorted(ROLE[c] for c in re.findall(r'[TRSD]', roles))
            if want != sorted(it['role']):
                diffs.append(f'roles {roles} -> {it["role"]}')
            if it['difficulty'] >= 4 and it.get('requires') != [draws]:
                diffs.append(f'requires {draws} -> {it.get("requires")}')
            if diffs:
                print(it['id'], '|', '; '.join(diffs))
print(f'{n} items compared, {miss} without a row')
