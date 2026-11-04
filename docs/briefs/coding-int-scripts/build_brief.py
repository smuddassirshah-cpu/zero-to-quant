import ast, json, re
STEM = {'l1': 'l1.py', 'l2': 'l2.py', 'l3': 'l3.py', 'l4': 'l4.py', 'lx': 'l_extra.py'}
consts = {}
for stem, fn in STEM.items():
    tree = ast.parse(open(fn).read())
    d = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            try:
                v = ast.literal_eval(node.value)
            except Exception:
                try:
                    v = eval(compile(ast.Expression(node.value), fn, 'eval'), {}, dict(d))
                except Exception:
                    continue
            if isinstance(v, str): d[node.targets[0].id] = v
    consts[stem] = d
tests = {stem: json.load(open(f'{stem}_tests.json')) for stem in STEM}
text = ''.join(open(f'brief_part{i}.md').read() for i in range(5))
def fix_cs(t):
    return re.sub(r"\| \d+ \| `xs = \[0\] \* 100000; count_subarrays_sum_k\(xs, 0\)` \| `5000050000` \|", "| 10 | `xs = [0] * 200000; count_subarrays_sum_k(xs, 0)` | `20000100000` |", t)
def sub(m):
    kind, a, b = m.group(1), m.group(2), m.group(3)
    if kind == 'PY': return '```python\n' + consts[a][b].strip('\n') + '\n```'
    if kind == 'CPP': return '```cpp\n' + consts[a][b].strip('\n') + '\n```'
    if kind == 'T':
        t = tests[a][b]
        if (a, b) == ('l4', 'cs'): t = fix_cs(t)
        return t
for pat in (r'@@(PY):(\w+):(\w+)@@', r'@@(CPP):(\w+):(\w+)@@', r'@@(T):(\w+):(\w+)@@'):
    text = re.sub(pat, sub, text)
text = re.sub(r'@@FILE:([\w./-]+)@@', lambda m: '```text\n' + open(m.group(1)).read().rstrip('\n') + '\n```', text)
names = json.load(open('/home/user/zero-to-quant/app/content/courses/coding-int/course.json'))['lessonNames']
for k, v in names.items():
    old = f'### {k} ('
    assert old in text, k
    text = text.replace(old, f'### {k}: {v} (')
assert '@@' not in text, re.findall(r'@@[^@]*@@', text)[:5]
open('coding-int.md', 'w').write(text)
print(len(text.splitlines()), 'lines')
