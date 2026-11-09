"""Second read, git homework-3 h-ignore-options-repo.

1. The shipped matcher (prelude, learner code, postlude in one namespace, as code.js runs it)
   against real git on random .gitignore files: 150 files of 1 to 5 random patterns (negation,
   trailing slash, leading slash, middle slash, *, ?, [..], ** at start, middle and end) over a
   fixed tree of 40 paths. Real git is read two ways: `git check-ignore --stdin` and
   `git ls-files -o -i --exclude-standard` (what `git add .` leaves out).
2. The shipped solution, the starter, three reader solutions and eight reader plants on the
   14 hidden tests, through the shipped matcher and through real git.
Exit 0 only if the matcher agrees with git on every path of every file and every claim holds.
"""
import json, os, random, re, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
hw = json.load(open(os.path.join(ROOT, 'app', 'content', 'courses', 'git', 'homework-3.json')))
item = next(i for i in hw['items'] if i['id'] == 'h-ignore-options-repo')
W = item['widget']; T = W['tests']
fails = []


def check(c, m):
    print('ok  ' if c else 'FAIL', m)
    if not c:
        fails.append(m)


def matcher(text):
    ns = {}
    exec(W['prelude'], ns)
    exec('GITIGNORE = ' + repr(text), ns)
    exec(W['postlude'], ns)
    return ns['ignored']


def git_ignored(text, paths):
    tmp = tempfile.mkdtemp()
    env = dict(os.environ, GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_SYSTEM='/dev/null')
    subprocess.run(['git', 'init', '-q', tmp], check=True, env=env)
    for p in paths:
        full = os.path.join(tmp, p)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        if p != '.gitignore':
            open(full, 'w').write('x')
    open(os.path.join(tmp, '.gitignore'), 'w').write(text)
    ci = subprocess.run(['git', '-C', tmp, 'check-ignore', '--stdin'], input='\n'.join(paths) + '\n',
                        capture_output=True, text=True, env=env).stdout.split('\n')
    ls = subprocess.run(['git', '-C', tmp, 'ls-files', '-o', '-i', '--exclude-standard'],
                        capture_output=True, text=True, env=env).stdout.split('\n')
    shutil.rmtree(tmp)
    return {p: p in ci for p in paths}, {p: p in ls for p in paths}

TREE = ['.gitignore', 'a.txt', 'b.log', 'ab.txt', 'x/a.txt', 'x/b.log', 'x/y/a.txt', 'x/y/z/c.md',
        'y/a.txt', 'y/x/a.txt', 'y/x/b.log', 'data/README.md', 'data/raw/r.parquet', 'data/raw/s.csv',
        'data/clean/c.parquet', 'docs/data/d.md', 'figures/f.png', 'docs/figures/g.png', 'src/figures.py',
        'src/__pycache__/p.pyc', 'src/m/__pycache__/q.pyc', '__pycache__/t.pyc', '.env', '.env.local',
        '.env.example', 'notebooks/.ipynb_checkpoints/n.ipynb', 'notebooks/n.ipynb', '.venv/bin/python',
        'venv/bin/python', 'a/b/c/d.txt', 'a/c/d.txt', 'a/d.txt', 'b/a/d.txt', 'logs/2025/app.log',
        'build/out/x.o', 'tests/fixtures/f.parquet', 'tests/test_a.py', 'z1.txt', 'z2.txt', 'za.txt']
check(len(TREE) == 40, '40 paths in the tree')

NAMES = ['a', 'b', 'x', 'y', 'z', 'c', 'd', 'data', 'raw', 'docs', 'figures', 'src', 'logs', 'build',
         '__pycache__', '.env', '.venv', 'venv', 'tests', 'fixtures', 'notebooks', 'out', 'm', '2025']
GLOBS = ['*', '*.txt', '*.log', '*.parquet', '?.txt', 'z[12].txt', 'z[!1].txt', 'z[a-c].txt', '.env*',
         '*.md', 'a*', '*a*', '[ab].txt', 'README.md', 'd.txt', 'c.md', '*.py', '*.pyc', 'app.log']
rng = random.Random(1409)


def rand_pattern():
    k = rng.random()
    parts = [rng.choice(NAMES + GLOBS) for _ in range(rng.choice([1, 1, 2, 2, 3]))]
    r = rng.random()
    if r < 0.15:
        parts = ['**'] + parts
    elif r < 0.25 and len(parts) >= 2:
        parts.insert(1, '**')
    elif r < 0.35:
        parts = parts + ['**']
    p = '/'.join(parts)
    if rng.random() < 0.25:
        p = '/' + p
    if rng.random() < 0.3:
        p = p + '/'
    if rng.random() < 0.3:
        p = '!' + p
    return p

trials = 0; paths_seen = 0; mism_ci = []; mism_ls = []; pats = []
feats = {'neg': 0, 'trail': 0, 'lead': 0, 'dstar': 0, 'mid': 0, 'class': 0}
for trial in range(150):
    lines = [rand_pattern() for _ in range(rng.randint(1, 5))]
    pats += lines
    text = '\n'.join(lines) + '\n'
    ig = matcher(text)
    ci, ls = git_ignored(text, TREE)
    for p in TREE:
        paths_seen += 1
        m = bool(ig(p))
        if m != ci[p]:
            mism_ci.append((text, p, m, ci[p]))
        if m != ls[p]:
            mism_ls.append((text, p, m, ls[p]))
    trials += 1
for p in pats:
    feats['neg'] += p.startswith('!'); feats['trail'] += p.endswith('/'); feats['lead'] += p.lstrip('!').startswith('/')
    feats['dstar'] += '**' in p; feats['mid'] += '/' in p.strip('!/'); feats['class'] += '[' in p
print('patterns: %d, features: %s' % (len(pats), feats))
check(trials == 150 and len(pats) >= 300, '150 random .gitignore files, %d patterns, %d path checks' % (len(pats), paths_seen))
check(all(v >= 30 for v in feats.values()), 'each feature appears at least 30 times')
for x in mism_ci[:5]:
    print('  check-ignore mismatch', x)
for x in mism_ls[:5]:
    print('  ls-files mismatch', x)
check(not mism_ci, 'matcher agrees with git check-ignore on every path (%d mismatches)' % len(mism_ci))
check(not mism_ls, 'matcher agrees with git ls-files -o -i (%d mismatches)' % len(mism_ls))
# hand edge cases: escapes, trailing spaces, odd brackets, lone stars, comments
ODD = ['.gitignore', '#a', '!b', 'a*', 'a b', 'c ', ']x', '[y', 'q/r', 'q/s/r', 'k.txt', 'K.txt', 'w/k.txt', 'ab', 'a.b']
EDGE = ['\\#a', '#a', '\\!b', '!b', 'a\\*', 'a*', 'c\\ ', 'c ', 'a b', ']x', '[]]x', '[!a]x', '[y', '\\[y',
        '***', '**/', 'q/**/', '**/r', 'q/**', '/q/s/', '[k-l].txt', '[[:upper:]].txt', '[[:alpha:]]b', '?b', '*.TXT',
        'w/', '/k.txt', 'q/*/r', 'a?b', '[a-]b', 'a[.]b', '!', '/', '\\', 'k.txt\\']
edge_bad = []
for pat in EDGE:
    for extra in ['', '\n!w/k.txt', '\nk.txt\n!K.txt']:
        text = pat + extra + '\n'
        ig = matcher(text)
        ci, ls = git_ignored(text, ODD)
        for q in ODD:
            if bool(ig(q)) != ci[q] or bool(ig(q)) != ls[q]:
                edge_bad.append((text, q, bool(ig(q)), ci[q], ls[q]))
for x in edge_bad[:8]:
    print('  edge mismatch', x)
known = [x for x in edge_bad if x[0].startswith('[y\n') and x[1] == '[y' and x[2] and not x[3] and not x[4]]
check(len(known) == 3 and len(edge_bad) == 3, 'only known edge difference: an unclosed [ (pattern [y) matches the literal name [y in the matcher, nothing in git (git wildmatch aborts)')
check(len(edge_bad) == len(known), 'matcher agrees with git on every other path of %d hand edge files over %d odd names' % (len(EDGE) * 3, len(ODD)))
# how often a parent directory exclusion decides (the rule a matcher most often gets wrong)
TEST_PATHS = sorted(set(re.findall(r"'([^']+)'", ' '.join(t['call'] for t in T))) | {'.gitignore'})


def grade(text):
    ig = matcher(text)
    ns = {'ignored': ig}
    a = [eval(t['call'], ns) == eval(t['expect']) for t in T]
    ci, ls = git_ignored(text, TEST_PATHS)
    ns2 = {'ignored': lambda p: ci[p]}
    b = [eval(t['call'], ns2) == eval(t['expect']) for t in T]
    ns3 = {'ignored': lambda p: ls[p]}
    c = [eval(t['call'], ns3) == eval(t['expect']) for t in T]
    return a, b, c


def text_of(src):
    ns = {}
    exec(src, ns)
    return ns['GITIGNORE']

for name, src in [('shipped solution', W['solution'])]:
    a, b, c = grade(text_of(src))
    check(all(a) and all(b) and all(c), '%s passes 14 of 14 (matcher, check-ignore, ls-files)' % name)
a, b, c = grade(text_of(W['starter']))
check(a == b == c and not all(a), 'starter fails tests %s on all three' % [k + 1 for k, v in enumerate(a) if not v])

READERS = {
    'R1 /data/** with !/data/README.md, **/ caches': '/data/**\n!/data/README.md\n/figures\n**/__pycache__\n**/.ipynb_checkpoints\n/.venv\n/.env\n/.env.local\n',
    'R2 .env* then !.env.example, data/* nested': 'data/*\n!data/README.md\n/figures/*\n__pycache__\n.ipynb_checkpoints\n.venv/\n.env*\n!.env.example\n',
    'R3 data/**/* with negation, figures/** anchored': '/data/**/*\n!/data/README.md\nfigures/**\n!docs/figures/**\n__pycache__/\n.ipynb_checkpoints/\n.venv\n.env\n.env.local\n',
}
for name, text in READERS.items():
    a, b, c = grade(text)
    check(all(a) and all(b) and all(c), 'reader %s passes 14 of 14 (matcher, check-ignore, ls-files)' % name)

PLANTS = {
    'P1 data/** ignores the README too (no take-back)': 'data/**\n/figures/\n__pycache__/\n.ipynb_checkpoints/\n.venv/\n.env\n.env.local\n',
    'P2 !README.md before data/* (order wrong)': '!data/README.md\ndata/*\n/figures/\n__pycache__/\n.ipynb_checkpoints/\n.venv/\n.env\n.env.local\n',
    'P3 /src/__pycache__/ anchored to one folder': 'data/*\n!data/README.md\n/figures/\n/src/__pycache__/\n**/.ipynb_checkpoints/\n.venv/\n.env\n.env.local\n',
    'P4 figures* catches src/figures.py': 'data/*\n!data/README.md\nfigures*\n!docs/figures*\n__pycache__/\n.ipynb_checkpoints/\n.venv/\n.env\n.env.local\n',
    'P5 .env.* catches the template': 'data/*\n!data/README.md\n/figures/\n__pycache__/\n.ipynb_checkpoints/\n.venv/\n.env\n.env.*\n',
    'P6 today\'s files only': 'data/raw/chains_2025.parquet\ndata/clean/chains_2025.parquet\nfigures/smile.png\n__pycache__/\n.ipynb_checkpoints/\n.venv/\n.env\n.env.local\n',
    'P7 notebooks/.ipynb_checkpoints/ one level only': 'data/*\n!data/README.md\n/figures/\n__pycache__/\nnotebooks/.ipynb_checkpoints/\n.venv/\n.env\n.env.local\n',
    'P8 venv/ without the dot': 'data/*\n!data/README.md\n/figures/\n__pycache__/\n.ipynb_checkpoints/\nvenv/\n.env\n.env.local\n',
}
for name, text in PLANTS.items():
    a, b, c = grade(text)
    fa = [k + 1 for k, v in enumerate(a) if not v]
    check(fa and a == b == c, 'plant %s fails tests %s (matcher = check-ignore = ls-files)' % (name, fa))

# claims in the item text
check('git check-ignore' in item['prose'], 'prose names git check-ignore')
check(W['how'].startswith('Submit runs 14 hidden tests'), 'how: 14 hidden tests')
print('\nFAILURES: %d' % len(fails))
sys.exit(1 if fails else 0)
