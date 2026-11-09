"""Recompute every claim of git homework-3 `h-ignore-options-repo` (performance code task).

Route A: the item's own prelude/postlude matcher, exactly as the browser runs it.
Route B: a real Git repository holding every path, read with `git ls-files -o --exclude-standard`
(what `git add .` would pick up) and, as a third check, `git check-ignore --no-index`.
Run: python3 docs/reports/git-3-perf-numbers.py (needs git on PATH). Exits 0 when every check holds.
"""
import json, os, random, re, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
HW = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'git', 'homework-3.json')
REVIEW = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'git', 'review-3.json')
ITEM_ID = 'h-ignore-options-repo'
FAIL = []


def check(ok, msg):
    print(('ok   ' if ok else 'FAIL ') + msg)
    if not ok:
        FAIL.append(msg)


hw = json.load(open(HW))
items = {i['id']: i for i in hw['items']}
item = items[ITEM_ID]
w = item['widget']
tests, examples = w['tests'], w['examples']

# ---- shape -------------------------------------------------------------------
check(item.get('performance') == 'code' and w['kind'] == 'code' and w['language'] == 'python', 'code performance item in Python')
check(len(tests) >= 3 and len(tests) > len(examples), f'{len(tests)} tests > {len(examples)} examples')
check(len(tests) <= 15, 'at most 15 tests')
check(all({'call': e['call'], 'expect': e['expect']} in [{'call': t['call'], 'expect': t['expect']} for t in tests] for e in examples), 'every example is also a hidden test')
check(re.search(r'runs (\d+) hidden tests', w['how']).group(1) == str(len(tests)), 'how states the test count')
check(w['prelude'] == w['postlude'], 'postlude re-installs the same matcher as the prelude')
check(sum(1 for i in hw['items'] if i.get('performance')) == 1, 'one performance item in homework-3')
check(not any(i.get('performance') for i in json.load(open(REVIEW))['items']), 'none in review-3')
check(6 <= len(hw['items']) <= 12, f'homework-3 holds {len(hw["items"])} items (6 to 12)')
check(item['difficulty'] == 5, 'difficulty 5')
keys = item['feedback']['byKey']
check(all(1 <= int(k.split('-')[1]) <= len(tests) for k in keys), 'byKey keys name real tests')
for k, v in keys.items():
    n = k.split('-')[1]
    check(v.startswith('Test ' + n), f'{k} text names test {n}')


# ---- route A: the shipped matcher --------------------------------------------
def run_a(gitignore_src):
    """Run as the browser does: prelude, learner code, postlude, then each call."""
    ns = {}
    exec(w['prelude'], ns)
    exec(gitignore_src, ns)
    exec(w['postlude'], ns)
    return [eval(t['call'], ns) == eval(t['expect']) for t in tests], ns


# ---- route B: real git -------------------------------------------------------
def paths_in(call):
    return re.findall(r"'([^']+)'", call)


PROSE_PATHS = re.findall(r'`([^`]+)`', item['prose'])
ALL = sorted(set(p for t in tests for p in paths_in(t['call'])) | {
    p for p in PROSE_PATHS if ('/' in p or '.' in p) and not p.endswith('/') and ' ' not in p and p not in ('.gitignore',)
} | {'.gitignore'})
TMP = tempfile.mkdtemp(prefix='git3perf-')


def git_truth(gitignore_text):
    root = os.path.join(TMP, 'repo')
    if os.path.exists(root):
        shutil.rmtree(root)
    os.makedirs(root)
    subprocess.run(['git', 'init', '-q', root], check=True)
    for p in ALL:
        if p == '.gitignore':
            continue
        f = os.path.join(root, p)
        os.makedirs(os.path.dirname(f), exist_ok=True)
        open(f, 'w').write('x\n')
    open(os.path.join(root, '.gitignore'), 'w').write(gitignore_text)
    out = subprocess.run(['git', '-C', root, 'ls-files', '-z', '-o', '--exclude-standard'],
                         capture_output=True, check=True).stdout.decode()
    kept = set(x for x in out.split('\0') if x)
    by_ls = {p: p not in kept for p in ALL}
    ci = subprocess.run(['git', '-C', root, 'check-ignore', '--no-index', '-z', '--stdin'],
                        input=('\0'.join(ALL) + '\0').encode(), capture_output=True).stdout.decode()
    by_ci = {p: p in set(x for x in ci.split('\0') if x) for p in ALL}
    return by_ls, by_ci


def text_of(src):
    ns = {}
    exec(src, ns)
    return ns.get('GITIGNORE', '')


def run_b(src):
    by_ls, by_ci = git_truth(text_of(src))
    check(by_ls == by_ci, '  git ls-files and git check-ignore agree on every path')
    ns = {'ignored': lambda p: by_ls[p]}
    return [eval(t['call'], ns) == eval(t['expect']) for t in tests], by_ls


def g(lines):
    return 'GITIGNORE = """\n' + '\n'.join(lines) + '\n"""\n'


ALTERNATIVES = {
    'data/** and figures/* and stars': g(['data/**', '!data/README.md', 'figures/*', '**/__pycache__/', '*.pyc',
                                          '.ipynb_checkpoints', '/.venv/', '.env*', '!.env.example']),
    'anchored everything': g(['/data/*', '!/data/README.md', '/figures', '__pycache__', '.ipynb_checkpoints/',
                              '/.venv', '/.env', '/.env.local']),
    'data subfolders by pattern': g(['data/*/', 'data/*.parquet', 'data/*.csv', '/figures/', '__pycache__/',
                                     '.ipynb_checkpoints/', '.venv/', '.env', '.env.local']),
}
SOL_LINES = ['data/*', '!data/README.md', '/figures/', '__pycache__/', '.ipynb_checkpoints/', '.venv/', '.env', '.env.local']


def swap(old, new):
    return g([new if x == old else x for x in SOL_LINES] if new is not None else [x for x in SOL_LINES if x != old])


# planted wrong solutions: name -> (source, first failing test expected, 1-based)
WRONG = {
    "the lesson's file": (g(['data/', 'figures/', '__pycache__/', '.venv/', '.env']), 3),
    "data/ then !data/README.md": (swap('data/*', 'data/'), 3),
    "file types instead of data/": (g(['*.parquet', '*.csv'] + SOL_LINES[2:]), 5),
    "today's data subfolders only": (g(['data/raw/', 'data/clean/'] + SOL_LINES[2:]), 4),
    "today's files listed by name": (g(['data/raw/chains_2025.parquet', 'data/clean/chains_2025.parquet', 'figures/smile.png',
                                       'src/__pycache__/', 'notebooks/.ipynb_checkpoints/', '.venv/', '.env', '.env.local']), 4),
    "figures/ not anchored": (swap('/figures/', 'figures/'), 7),
    "figures* catches the script": (swap('/figures/', 'figures*'), 7),
    "src/__pycache__/ only": (swap('__pycache__/', 'src/__pycache__/'), 9),
    "checkpoints forgotten": (swap('.ipynb_checkpoints/', None), 10),
    ".env* catches the template": (g([x for x in SOL_LINES if x not in ('.env', '.env.local')] + ['.env*']), 13),
    "paper key forgotten": (swap('.env.local', None), 12),
    "comment after a pattern": (swap('data/*', 'data/*  # downloads'), 1),
    "all dotfiles": (g(SOL_LINES + ['.*']), 13),
    "venv forgotten": (swap('.venv/', None), 11),
}

print('\n-- solution, starter, alternatives (route A and route B) --')
for name, src in [('solution', w['solution']), ('starter', w['starter'])] + list(ALTERNATIVES.items()):
    ra, _ = run_a(src)
    rb, truth = run_b(src)
    check(ra == rb, f'{name}: shipped matcher agrees with git on all {len(tests)} tests')
    if name == 'starter':
        check(not all(ra), f'starter fails {ra.count(False)} of {len(tests)} tests')
    else:
        check(all(ra) and all(rb), f'{name}: passes {ra.count(True)} of {len(tests)} tests')

print('\n-- planted wrong solutions --')
for name, (src, first) in WRONG.items():
    ra, _ = run_a(src)
    rb, _ = run_b(src)
    got = ra.index(False) + 1 if False in ra else None
    check(ra == rb and got == first, f'{name}: fails {ra.count(False)} tests, first test {got} (expected {first}), git agrees')
    if f'test-{got}' in keys:
        print(f'     feedback shown: {keys["test-" + str(got)][:70]}...')

print('\n-- prose: every listed file lands on its stated side under the solution (git) --')
prose = item['prose']
commit_part = prose.split('**Commit**')[1].split('**Keep out**')[0]
keep_part = prose.split('**Keep out**')[1].split('The rules must')[0]
commit_paths = [p for p in re.findall(r'`([^`]+)`', commit_part)]
keep_paths = [p for p in re.findall(r'`([^`]+)`', keep_part) if not p.endswith('/')]
_, truth = run_b(w['solution'])
for p in commit_paths:
    check(truth[p] is False, f'commit: {p} is not ignored')
for p in keep_paths:
    check(truth[p] is True, f'keep out: {p} is ignored')
check(sorted(commit_paths + keep_paths + [p for p in re.findall(r'`([^`]+)`', keep_part) if p.endswith('/')]) ==
      sorted(re.findall(r'`([^`]+)`', commit_part + keep_part)), 'every path in the two lists was checked')
# test expectations follow the stated rules (independent of any .gitignore)


def rule(p):
    top = p.split('/')[0]
    parts = p.split('/')
    if p in ('data/README.md',):
        return False
    if top == 'data':
        return True
    if top == 'figures':
        return True
    if top == '.venv':
        return True
    if p in ('.env', '.env.local'):
        return True
    if '__pycache__' in parts[:-1] or '.ipynb_checkpoints' in parts[:-1]:
        return True
    return False


for t in tests:
    ns = {'ignored': rule}
    check(eval(t['call'], ns) == eval(t['expect']), f'expectation follows the prose rules: {t["call"][:60]}')

print('\n-- fuzz: shipped matcher against git on random .gitignore files --')
POOL = ['data/', 'data/*', 'data/**', '/data/', '!data/README.md', '!README.md', 'figures/', '/figures/', 'figures/*',
        '/figures', 'figures', 'figures*', '__pycache__/', '*.pyc', 'src/__pycache__/', '**/__pycache__/',
        '.ipynb_checkpoints/', '*checkpoint*', '.venv/', '/.venv', '.env', '.env*', '!.env.example', '.env.local',
        '.*', '!.gitignore', '*.parquet', '*.csv', '!tests/fixtures/*.parquet', '!tests/**', 'data/raw/', 'data/*/',
        'data/**/*.csv', '**/*.csv', 'src/**/*.pyc', 'x[0-9]*', '[a-z]*.md', 'docs/**/', '*.md', '!*.md', '!data/',
        '/*', '!/src/', '**', 'data/*  # downloads', '# comment', '', 'd?ta/', 'data/[rc]*/', '\\#x', '*.py   ']
rnd = random.Random(20261109)
mism = 0
N = 250
for _ in range(N):
    text = '\n'.join(rnd.choice(POOL) for _ in range(rnd.randint(1, 8))) + '\n'
    ns = {}
    exec(w['prelude'], ns)
    mine = {p: ns['_zq_ignored'](p, text) for p in ALL}
    by_ls, _ = git_truth(text)
    mism += mine != by_ls
check(mism == 0, f'{N} random files over {len(ALL)} paths: {mism} mismatches')

shutil.rmtree(TMP)
print(f'\n{len(FAIL)} failures')
sys.exit(1 if FAIL else 0)
