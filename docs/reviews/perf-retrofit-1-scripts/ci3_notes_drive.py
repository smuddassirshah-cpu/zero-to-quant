"""coding-int/homework-3 h3-notes-drive: reader's own design (parent pointers,
sizes pushed up by walking parents), shipped solution, starter and reader-planted
slips against every case, with times. Also asks which planted slips reach only
test 10, whose byKey text says "timed out"."""
from harness import item, run, check, finish

_, it = item('coding-int', 'homework-3', 'h3-notes-drive')
w = it['widget']
cases = w['examples'] + w['tests']

mine = '''
class Entry:
    def __init__(self, parent=None, name=''):
        self.parent, self.name = parent, name
        self.kids = None          # dict for a folder, None for a file
        self.data = ''
        self.size = 0

def _parts(path):
    return tuple(p for p in path.split('/') if p)

class NotesDrive:
    def __init__(self):
        self.top = Entry()
        self.top.kids = {}

    def _find(self, parts):
        e = self.top
        for p in parts:
            if e.kids is None or p not in e.kids:
                return None
            e = e.kids[p]
        return e

    def _dirs(self, parts):
        e = self.top
        for p in parts:
            if p not in e.kids:
                f = Entry(e, p)
                f.kids = {}
                e.kids[p] = f
            e = e.kids[p]
        return e

    def _bump(self, e, d):
        while e is not None:
            e.size += d
            e = e.parent

    def mkdir(self, path):
        self._dirs(_parts(path))

    def write(self, path, text):
        ps = _parts(path)
        folder = self._dirs(ps[:-1])
        f = folder.kids.get(ps[-1])
        if f is None:
            f = folder.kids[ps[-1]] = Entry(folder, ps[-1])
        self._bump(f, len(text) - f.size)
        f.data = text

    def read(self, path):
        e = self._find(_parts(path))
        return e.data if e is not None and e.kids is None else None

    def ls(self, path):
        e = self._find(_parts(path))
        if e is None:
            return []
        return [e.name] if e.kids is None else sorted(e.kids)

    def rm(self, path):
        e = self._find(_parts(path))
        if e is None or e is self.top:
            return
        self._bump(e.parent, -e.size)
        del e.parent.kids[e.name]

    def mv(self, src, dst):
        s, d = _parts(src), _parts(dst)
        e = self._find(s)
        if e is None or not s or self._find(d) is not None or d[:len(s)] == s:
            return False
        self._bump(e.parent, -e.size)
        del e.parent.kids[e.name]
        folder = self._dirs(d[:-1])
        e.parent, e.name = folder, d[-1]
        folder.kids[d[-1]] = e
        self._bump(folder, e.size)
        return True

    def size(self, path):
        e = self._find(_parts(path))
        return 0 if e is None else e.size
'''
for name, code in [('shipped solution', w['solution']), ('reader design', mine)]:
    res = run(code, w, cases)
    check(all(r[0] for r in res), f'{name} passes all {len(cases)} cases, test 10 in {res[-1][1]:.3f} s')

res = run(w['starter'], w, w['tests'])
check(not any(r[0] for r in res), 'starter fails every hidden test')
check(w['examples'] == w['tests'][:2], 'note: hidden tests 1 and 2 repeat the two examples, so 8 tests are unseen')

S = w['solution']
def mut(old, new):
    assert S.count(old) == 1, old
    return S.replace(old, new)

caught = {
    'ls of a missing path gives None': mut("        if chain is None:\n            return []\n", "        if chain is None:\n            return None\n"),
    'read of a folder gives the empty string': mut(
        "        return None if chain is None else chain[-1].text",
        "        return None if chain is None else (chain[-1].text if chain[-1].text is not None else '')"),
    'mv copies, leaving src in place': mut("        del chain[-2].children[s[-1]]\n        target", "        target"),
    'mkdir replaces an existing folder': mut(
        "    def mkdir(self, path):\n        self._make(self._names(path))",
        "    def mkdir(self, path):\n        names = self._names(path)\n        if names:\n            chain = self._make(names[:-1])\n            chain[-1].children[names[-1]] = _Node()"),
}
first_only_10 = []
for name, code in caught.items():
    hid = run(code, w, w['tests'])
    bad = [k + 1 for k, r in enumerate(hid) if not r[0]]
    check(bool(bad), f'planted "{name}" caught by hidden tests {bad}')
    if bad and bad[0] == 10:
        first_only_10.append(name)
print('slips whose first failure is test 10 (shown "Test 10 timed out"):', first_only_10)

# size of a file: the prose says "the files at or below path", so a file has its own length.
size_file = mut(
    "        return 0 if chain is None else chain[-1].total",
    "        return 0 if chain is None or chain[-1].text is not None else chain[-1].total")
hid = run(size_file, w, w['tests'])
bad = [k + 1 for k, r in enumerate(hid) if not r[0]]
print(f'size of a file returns 0: fails hidden tests {bad} (finding CI3-b if empty)')
finish()
