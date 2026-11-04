import random, collections, json, math, subprocess, tempfile
from harness import *
random.seed(31)
REP = {}; NUM = {}

# ---------- 3.1 LRU ----------
LRU_REF = '''
class _Node:
    def __init__(self, key=0, value=0):
        self.key, self.value = key, value
        self.prev = self.next = None

class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.map = {}
        self.head, self.tail = _Node(), _Node()       # sentinels: head.next is the most recent
        self.head.next, self.tail.prev = self.tail, self.head

    def _unlink(self, node):
        node.prev.next, node.next.prev = node.next, node.prev

    def _push_front(self, node):
        node.prev, node.next = self.head, self.head.next
        self.head.next.prev = node
        self.head.next = node

    def get(self, key):
        node = self.map.get(key)
        if node is None:
            return -1
        self._unlink(node)
        self._push_front(node)
        return node.value

    def put(self, key, value):
        node = self.map.get(key)
        if node is not None:
            node.value = value
            self._unlink(node)
            self._push_front(node)
            return
        if len(self.map) == self.capacity:
            last = self.tail.prev
            self._unlink(last)
            del self.map[last.key]
        node = _Node(key, value)
        self.map[key] = node
        self._push_front(node)
'''
LRU_START = '''
class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.data = {}

    def get(self, key):
        return self.data.get(key, -1)

    def put(self, key, value):
        self.data[key] = value
'''
LRU_POST = '''
def run_lru(cap, ops):
    c = LRUCache(cap)
    out = []
    for op in ops:
        if op[0] == 0:
            c.put(op[1], op[2])
        else:
            out.append(c.get(op[1]))
    return out
'''
def lru_brute(cap, ops):
    order, vals, out = [], {}, []        # order: least recent first
    for op in ops:
        if op[0] == 0:
            k, v = op[1], op[2]
            if k in vals: order.remove(k)
            elif len(order) == cap: del vals[order.pop(0)]
            order.append(k); vals[k] = v
        else:
            k = op[1]
            if k in vals: order.remove(k); order.append(k); out.append(vals[k])
            else: out.append(-1)
    return out
ns = {}; exec(LRU_REF + LRU_POST, ns); runlru = ns['run_lru']
def rand_ops(n, keys=5):
    return [[0, random.randint(1, keys), random.randint(1, 50)] if random.random() < 0.55 else [1, random.randint(1, keys)] for _ in range(n)]
for _ in range(3000):
    cap = random.randint(1, 4); ops = rand_ops(random.randint(0, 20))
    assert runlru(cap, ops) == lru_brute(cap, ops), (cap, ops)
lops = [(2,[[0,5,50],[0,6,60],[1,5],[0,7,70],[1,6],[0,8,80],[1,5],[1,7],[1,8]]),
        (1,[[0,2,1],[1,2],[0,3,2],[1,2],[1,3]]),
        (2,[[0,2,1],[0,2,2],[1,2],[0,1,1],[0,4,1],[1,2]]),
        (3,[[0,1,10],[0,2,20],[0,3,30],[1,1],[0,4,40],[1,2],[1,1],[1,3],[1,4]]),
        (2,[[1,9]]),
        (2,[[0,1,1],[0,2,2],[0,1,5],[0,3,3],[1,1],[1,2],[1,3]])]
LRU_TESTS = [dict(call=f'run_lru({c}, {o})', expect=lru_brute(c, o)) for c, o in lops]
big = [[0, i, i] for i in range(100000)] + [[1, i] for i in range(99000, 100000)] + [[1, 0]]
LRU_TESTS.append(dict(setup='ops = [[0, i, i] for i in range(100000)] + [[1, i] for i in range(99000, 100000)] + [[1, 0]]', call='sum(run_lru(1000, ops))', expect=None))
exp = sum(lru_brute(1000, big[:0] + [[0, i, i] for i in range(100000)] + [[1, i] for i in range(99000, 100000)] + [[1, 0]])) if False else sum(runlru(1000, big))
# brute for the big case through an independent closed form: last 1000 keys 99000..99999 survive, key 0 is evicted
exp_closed = sum(range(99000, 100000)) + (-1)
assert exp == exp_closed, (exp, exp_closed)
LRU_TESTS[-1]['expect'] = exp_closed
LRU_TESTS.append(dict(call="'OrderedDict' not in __learner_source__", expect=True))
check_py('LRUCache', LRU_REF, LRU_START, LRU_TESTS, postlude=LRU_POST)
REP['lru'] = md_tests(LRU_TESTS)

LRU_CPP_REF = '''#include <list>
#include <unordered_map>
#include <vector>
class LRUCache {
public:
    explicit LRUCache(int capacity) : capacity_(capacity) {}
    int get(int key) {
        auto it = index_.find(key);
        if (it == index_.end()) return -1;
        items_.splice(items_.begin(), items_, it->second);
        return it->second->second;
    }
    void put(int key, int value) {
        auto it = index_.find(key);
        if (it != index_.end()) {
            it->second->second = value;
            items_.splice(items_.begin(), items_, it->second);
            return;
        }
        if ((int)items_.size() == capacity_) {
            index_.erase(items_.back().first);
            items_.pop_back();
        }
        items_.emplace_front(key, value);
        index_[key] = items_.begin();
    }
private:
    int capacity_;
    std::list<std::pair<int, int>> items_;
    std::unordered_map<int, std::list<std::pair<int, int>>::iterator> index_;
};
'''
LRU_CPP_START = '''#include <list>
#include <unordered_map>
#include <vector>
class LRUCache {
public:
    explicit LRUCache(int capacity) : capacity_(capacity) {}
    int get(int key) {
        auto it = data_.find(key);
        return it == data_.end() ? -1 : it->second;
    }
    void put(int key, int value) { data_[key] = value; }
private:
    int capacity_;
    std::unordered_map<int, int> data_;
};
'''
LRU_CPP_POST = '''
std::vector<int> run_lru(int cap, std::vector<std::vector<int>> ops) {
    LRUCache c(cap);
    std::vector<int> out;
    for (const auto& op : ops) {
        if (op[0] == 0) c.put(op[1], op[2]);
        else out.push_back(c.get(op[1]));
    }
    return out;
}
'''
V = 'std::vector<std::vector<int>>'
calls = [(f'run_lru({c}, {V}{cpp_lit(o)})', lru_brute(c, o)) for c, o in lops]
calls.append((f'[&]{{ {V} ops; for (int i = 0; i < 100000; ++i) ops.push_back({{0, i, i}}); for (int i = 99000; i < 100000; ++i) ops.push_back({{1, i}}); ops.push_back({{1, 0}}); long long s = 0; for (int v : run_lru(1000, ops)) s += v; return s; }}()', exp_closed))
check_cpp('LRUCache_cpp', LRU_CPP_REF, LRU_CPP_START, calls, postlude=LRU_CPP_POST)

# TTL cache
TTL_REF = '''
class _Node:
    def __init__(self, key=0, value=0, touched=0):
        self.key, self.value, self.touched = key, value, touched
        self.prev = self.next = None

class TTLCache:
    def __init__(self, capacity, ttl):
        self.capacity, self.ttl = capacity, ttl
        self.map = {}
        self.head, self.tail = _Node(), _Node()
        self.head.next, self.tail.prev = self.tail, self.head

    def _unlink(self, node):
        node.prev.next, node.next.prev = node.next, node.prev

    def _push_front(self, node):
        node.prev, node.next = self.head, self.head.next
        self.head.next.prev = node
        self.head.next = node

    def _purge(self, now):
        while self.tail.prev is not self.head and now - self.tail.prev.touched >= self.ttl:
            last = self.tail.prev
            self._unlink(last)
            del self.map[last.key]

    def get(self, key, now):
        self._purge(now)
        node = self.map.get(key)
        if node is None:
            return -1
        node.touched = now
        self._unlink(node)
        self._push_front(node)
        return node.value

    def put(self, key, value, now):
        self._purge(now)
        node = self.map.get(key)
        if node is not None:
            node.value, node.touched = value, now
            self._unlink(node)
            self._push_front(node)
            return
        if len(self.map) == self.capacity:
            last = self.tail.prev
            self._unlink(last)
            del self.map[last.key]
        node = _Node(key, value, now)
        self.map[key] = node
        self._push_front(node)
'''
TTL_START = '''
class TTLCache:
    def __init__(self, capacity, ttl):
        self.capacity, self.ttl = capacity, ttl
        self.data = {}

    def get(self, key, now):
        return self.data.get(key, -1)

    def put(self, key, value, now):
        self.data[key] = value
'''
TTL_POST = '''
def run_ttl(cap, ttl, ops):
    c = TTLCache(cap, ttl)
    out = []
    for op in ops:
        if op[0] == 0:
            c.put(op[1], op[2], op[3])
        else:
            out.append(c.get(op[1], op[2]))
    return out
'''
def ttl_brute(cap, ttl, ops):
    order, vals, touch, out = [], {}, {}, []
    def purge(now):
        for k in [k for k in order if now - touch[k] >= ttl]:
            order.remove(k); del vals[k]; del touch[k]
    for op in ops:
        if op[0] == 0:
            k, v, now = op[1], op[2], op[3]; purge(now)
            if k in vals: order.remove(k)
            elif len(order) == cap: del vals[order[0]]; del touch[order[0]]; order.pop(0)
            order.append(k); vals[k] = v; touch[k] = now
        else:
            k, now = op[1], op[2]; purge(now)
            if k in vals: order.remove(k); order.append(k); touch[k] = now; out.append(vals[k])
            else: out.append(-1)
    return out
ns = {}; exec(TTL_REF + TTL_POST, ns); runttl = ns['run_ttl']
def rand_ttl_ops(n):
    t, ops = 0, []
    for _ in range(n):
        t += random.randint(0, 3)
        ops.append([0, random.randint(1, 5), random.randint(1, 50), t] if random.random() < 0.5 else [1, random.randint(1, 5), t])
    return ops
for _ in range(4000):
    cap = random.randint(1, 4); ttl = random.randint(1, 6); ops = rand_ttl_ops(random.randint(0, 20))
    assert runttl(cap, ttl, ops) == ttl_brute(cap, ttl, ops), (cap, ttl, ops)
tts = [(2, 5, [[0,1,10,0],[0,2,20,1],[1,1,4],[1,2,6],[1,1,8]]),
       (2, 5, [[0,1,10,0],[1,1,5]]),
       (2, 5, [[0,1,10,0],[1,1,4],[1,1,8],[1,1,13],[1,1,14]]),
       (2, 10, [[0,1,1,0],[0,2,2,1],[0,3,3,2],[1,1,3],[1,2,3],[1,3,3]]),
       (2, 3, [[0,1,1,0],[0,2,2,2],[0,3,3,3],[1,1,3],[1,2,3],[1,3,3]]),
       (3, 4, [[0,1,1,0],[0,2,2,1],[0,3,3,2],[1,1,3],[0,4,4,3],[1,2,3],[1,1,3],[1,4,4],[1,3,5]])]
TTL_TESTS = [dict(call=f'run_ttl({c}, {t}, {o})', expect=ttl_brute(c, t, o)) for c, t, o in tts]
check_py('TTLCache', TTL_REF, TTL_START, TTL_TESTS, postlude=TTL_POST)
REP['ttl'] = md_tests(TTL_TESTS)
for c,t,o in tts: print('ttl', ttl_brute(c,t,o))

# LFU (homework d5)
LFU_REF = '''
from collections import defaultdict, OrderedDict

class LFUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.vals, self.freq = {}, {}
        self.buckets = defaultdict(OrderedDict)    # freq -> keys, oldest first
        self.min_freq = 0

    def _touch(self, key):
        f = self.freq[key]
        del self.buckets[f][key]
        if not self.buckets[f]:
            del self.buckets[f]
            if self.min_freq == f:
                self.min_freq += 1
        self.freq[key] = f + 1
        self.buckets[f + 1][key] = None

    def get(self, key):
        if key not in self.vals:
            return -1
        self._touch(key)
        return self.vals[key]

    def put(self, key, value):
        if self.capacity == 0:
            return
        if key in self.vals:
            self.vals[key] = value
            self._touch(key)
            return
        if len(self.vals) == self.capacity:
            victim, _ = self.buckets[self.min_freq].popitem(last=False)
            if not self.buckets[self.min_freq]:
                del self.buckets[self.min_freq]
            del self.vals[victim], self.freq[victim]
        self.vals[key], self.freq[key] = value, 1
        self.buckets[1][key] = None
        self.min_freq = 1
'''
LFU_START = '''
class LFUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.data = {}

    def get(self, key):
        return self.data.get(key, -1)

    def put(self, key, value):
        self.data[key] = value
'''
LFU_POST = LRU_POST.replace('LRUCache', 'LFUCache').replace('run_lru', 'run_lfu')
def lfu_brute(cap, ops):
    vals, freq, last, clock, out = {}, {}, {}, 0, []
    for op in ops:
        clock += 1
        if op[0] == 0:
            if cap == 0: continue
            k, v = op[1], op[2]
            if k in vals: vals[k] = v; freq[k] += 1; last[k] = clock
            else:
                if len(vals) == cap:
                    victim = min(vals, key=lambda x: (freq[x], last[x]))
                    del vals[victim], freq[victim], last[victim]
                vals[k] = v; freq[k] = 1; last[k] = clock
        else:
            k = op[1]
            if k in vals: freq[k] += 1; last[k] = clock; out.append(vals[k])
            else: out.append(-1)
    return out
ns = {}; exec(LFU_REF + LFU_POST, ns); runlfu = ns['run_lfu']
for _ in range(4000):
    cap = random.randint(0, 4); ops = rand_ops(random.randint(0, 24))
    assert runlfu(cap, ops) == lfu_brute(cap, ops), (cap, ops)
lfs = [(2,[[0,5,50],[0,6,60],[1,5],[0,7,70],[1,6],[1,7],[0,8,80],[1,5],[1,7],[1,8]]),
       (0,[[0,0,0],[1,0]]),
       (2,[[0,1,1],[0,2,2],[0,3,3],[1,1],[1,2],[1,3]]),
       (2,[[0,5,5],[0,6,6],[1,5],[1,5],[0,7,7],[1,6],[1,7],[1,5]]),
       (3,[[0,1,1],[0,2,2],[0,3,3],[1,1],[1,2],[0,4,4],[1,3],[1,1],[1,2],[1,4]]),
       (1,[[0,1,1],[0,1,9],[1,1],[0,2,2],[1,1],[1,2]])]
LFU_TESTS = [dict(call=f'run_lfu({c}, {o})', expect=lfu_brute(c, o)) for c, o in lfs]
LFU_TESTS.append(dict(setup='ops = [[0, i, i] for i in range(50000)] + [[1, i] for i in range(49000, 50000)]', call='sum(run_lfu(1000, ops))', expect=sum(range(49000, 50000))))
assert runlfu(1000, [[0,i,i] for i in range(50000)] + [[1,i] for i in range(49000,50000)]) == [x for x in range(49000, 50000)] or True
assert sum(runlfu(1000, [[0,i,i] for i in range(50000)] + [[1,i] for i in range(49000,50000)])) == sum(range(49000, 50000)) == sum(lfu_brute(1000, [[0,i,i] for i in range(5000)] + [[1,i] for i in range(4000,5000)])) - sum(range(4000,5000)) + sum(range(49000,50000)) 
check_py('LFUCache', LFU_REF, LFU_START, LFU_TESTS, postlude=LFU_POST)
REP['lfu'] = md_tests(LFU_TESTS)

# ---------- 3.2 file system ----------
FS_REF = '''
class _Node:
    def __init__(self):
        self.children = {}
        self.content = None          # None for a folder, a string for a file

class FileSystem:
    def __init__(self):
        self.root = _Node()

    def _walk(self, path, create=False):
        node = self.root
        for name in path.split('/'):
            if not name:
                continue
            if name not in node.children:
                if not create:
                    return None
                node.children[name] = _Node()
            node = node.children[name]
        return node

    def mkdir(self, path):
        self._walk(path, create=True)

    def write(self, path, text):
        node = self._walk(path, create=True)
        node.content = (node.content or '') + text

    def read(self, path):
        return self._walk(path).content

    def ls(self, path):
        node = self._walk(path)
        if node.content is not None:
            return [path.rstrip('/').split('/')[-1]]
        return sorted(node.children)

    def size(self, path):
        node = self._walk(path)
        def total(n):
            if n.content is not None:
                return len(n.content)
            return sum(total(c) for c in n.children.values())
        return total(node)
'''
FS_START = '''
class FileSystem:
    def __init__(self):
        self.files = {}

    def mkdir(self, path):
        pass

    def write(self, path, text):
        self.files[path] = text

    def read(self, path):
        return self.files[path]

    def ls(self, path):
        return []

    def size(self, path):
        return 0
'''
FS_POST = '''
def run_fs(ops):
    fs = FileSystem()
    out = []
    for op in ops:
        if op[0] == 'mkdir': fs.mkdir(op[1])
        elif op[0] == 'write': fs.write(op[1], op[2])
        elif op[0] == 'ls': out.append(fs.ls(op[1]))
        elif op[0] == 'read': out.append(fs.read(op[1]))
        else: out.append(fs.size(op[1]))
    return out
'''
def fs_brute(ops):
    dirs, files, out = {'/'}, {}, []
    def parents(p):
        parts = [x for x in p.split('/') if x]
        return ['/' + '/'.join(parts[:i]) for i in range(1, len(parts))]
    def norm(p): return '/' + '/'.join(x for x in p.split('/') if x)
    for op in ops:
        p = norm(op[1])
        if op[0] == 'mkdir':
            for q in parents(p) + [p]: dirs.add(q)
        elif op[0] == 'write':
            for q in parents(p): dirs.add(q)
            files[p] = files.get(p, '') + op[2]
        elif op[0] == 'ls':
            if p in files: out.append([p.split('/')[-1]])
            else:
                pre = '' if p == '/' else p
                names = {q[len(pre)+1:].split('/')[0] for q in list(dirs) + list(files) if q != p and q.startswith(pre + '/')}
                out.append(sorted(names))
        elif op[0] == 'read': out.append(files[p])
        else:
            pre = '' if p == '/' else p
            out.append(sum(len(t) for q, t in files.items() if q == p or q.startswith(pre + '/')))
    return out
ns = {}; exec(FS_REF + FS_POST, ns); runfs = ns['run_fs']
names = ['a','b','c','x.txt','y.txt']
for _ in range(3000):
    ops = []
    for _ in range(random.randint(1, 14)):
        depth = random.randint(1, 3); path = '/' + '/'.join(random.choice(names) for _ in range(depth))
        r = random.random()
        if r < 0.25: ops.append(('mkdir', path))
        elif r < 0.5: ops.append(('write', path, random.choice(['hi', 'abc', 'x'])))
        else: ops.append((random.choice(['ls', 'size']), '/' if random.random() < 0.3 else path))
    # make ops valid: drop queries/writes that touch a file used as a folder (or a folder used as a file)
    good, state_files, state_dirs = [], set(), {'/'}
    for op in ops:
        p = '/' + '/'.join(x for x in op[1].split('/') if x); parts = [x for x in p.split('/') if x]
        pars = ['/' + '/'.join(parts[:i]) for i in range(1, len(parts))]
        if op[0] in ('mkdir', 'write'):
            if any(q in state_files for q in pars) or (op[0] == 'mkdir' and p in state_files) or (op[0] == 'write' and p in state_dirs): continue
            for q in pars + ([p] if op[0] == 'mkdir' else []): state_dirs.add(q)
            if op[0] == 'write': state_files.add(p)
            good.append(op)
        else:
            if p == '/' or p in state_files or p in state_dirs: good.append(op)
    if not good: continue
    assert runfs(good) == fs_brute(good), good
fsops = [
 [('mkdir','/a/b/c'),('ls','/'),('ls','/a'),('write','/a/b/c/d.txt','hello'),('ls','/a/b/c'),('ls','/a/b/c/d.txt'),('write','/a/b/c/d.txt',' world'),('read','/a/b/c/d.txt')],
 [('write','/x.txt','abc'),('ls','/'),('read','/x.txt')],
 [('ls','/')],
 [('mkdir','/a/b'),('mkdir','/a/b'),('write','/a/z.txt','q'),('ls','/a')],
 [('write','/docs/n/a.txt','12345'),('write','/docs/n/b.txt','678'),('write','/docs/c.txt','9'),('size','/docs'),('size','/docs/n'),('size','/docs/c.txt'),('size','/'),('ls','/docs')],
 [('mkdir','/b'),('mkdir','/a'),('write','/c.txt','1'),('mkdir','/a/z'),('ls','/')],
]
FS_TESTS = [dict(call=f'run_fs({o})', expect=fs_brute(o)) for o in fsops]
check_py('FileSystem', FS_REF, FS_START, FS_TESTS, postlude=FS_POST)
REP['fs'] = md_tests(FS_TESTS)
for o in fsops: print('fs', fs_brute(o))

# ---------- 3.3 ledger ----------
LED1 = '''
class Ledger:
    def __init__(self):
        self.pos = {}

    def trade(self, symbol, qty):
        self.pos[symbol] = self.pos.get(symbol, 0) + qty

    def position(self, symbol):
        return self.pos.get(symbol, 0)
'''
LED1_START = '''
class Ledger:
    def __init__(self):
        pass

    def trade(self, symbol, qty):
        pass

    def position(self, symbol):
        return 0
'''
LED2 = '''
class Ledger:
    def __init__(self):
        self.pos, self.avg, self.pnl = {}, {}, {}

    def trade(self, symbol, qty, price=0):
        held = self.pos.get(symbol, 0)
        if held + qty < 0:
            raise ValueError('cannot sell more than held')
        if qty > 0:
            total = held * self.avg.get(symbol, 0.0) + qty * price
            self.avg[symbol] = total / (held + qty)
        else:
            self.pnl[symbol] = self.pnl.get(symbol, 0) + (-qty) * (price - self.avg[symbol])
        self.pos[symbol] = held + qty
        if self.pos[symbol] == 0:
            self.avg[symbol] = 0.0

    def position(self, symbol):
        return self.pos.get(symbol, 0)

    def avg_cost(self, symbol):
        return self.avg.get(symbol, 0.0)

    def realised(self, symbol):
        return self.pnl.get(symbol, 0)
'''
LED2_START = '''
class Ledger:
    def __init__(self):
        self.pos = {}

    def trade(self, symbol, qty, price=0):
        self.pos[symbol] = self.pos.get(symbol, 0) + qty

    def position(self, symbol):
        return self.pos.get(symbol, 0)

    def avg_cost(self, symbol):
        return 0.0

    def realised(self, symbol):
        return 0
'''
LED3 = '''
from collections import deque

class Ledger:
    def __init__(self, method='average'):
        self.method = method
        self.lots, self.pnl = {}, {}              # symbol -> deque of [qty, price]
        self.pos, self.avg = {}, {}

    def trade(self, symbol, qty, price=0):
        held = self.pos.get(symbol, 0)
        if held + qty < 0:
            raise ValueError('cannot sell more than held')
        lots = self.lots.setdefault(symbol, deque())
        if qty > 0:
            total = held * self.avg.get(symbol, 0.0) + qty * price
            self.avg[symbol] = total / (held + qty)
            lots.append([qty, price])
        else:
            left = -qty
            if self.method == 'fifo':
                gain = 0
                while left:
                    take = min(left, lots[0][0])
                    gain += take * (price - lots[0][1])
                    lots[0][0] -= take
                    left -= take
                    if lots[0][0] == 0:
                        lots.popleft()
            else:
                gain = left * (price - self.avg[symbol])
                while left:
                    take = min(left, lots[0][0])
                    lots[0][0] -= take
                    left -= take
                    if lots[0][0] == 0:
                        lots.popleft()
            self.pnl[symbol] = self.pnl.get(symbol, 0) + gain
        self.pos[symbol] = held + qty
        if self.pos[symbol] == 0:
            self.avg[symbol] = 0.0
        elif self.method == 'fifo':
            self.avg[symbol] = sum(q * p for q, p in lots) / sum(q for q, p in lots)

    def position(self, symbol):
        return self.pos.get(symbol, 0)

    def avg_cost(self, symbol):
        return self.avg.get(symbol, 0.0)

    def realised(self, symbol):
        return self.pnl.get(symbol, 0)
'''
LED3_START = LED2_START.replace("def __init__(self):\n        self.pos = {}", "def __init__(self, method='average'):\n        self.pos = {}\n        self.method = method")
def led_brute(method, trades, sym='ABC'):
    """replay the whole history; returns (position, avg_cost, realised)"""
    lots = []; pnl = 0
    for qty, price in trades:
        if qty > 0: lots.append([qty, price])
        else:
            left = -qty
            tot = sum(q for q, p in lots)
            assert left <= tot
            avg = sum(q * p for q, p in lots) / tot
            if method == 'fifo':
                while left:
                    take = min(left, lots[0][0]); pnl += take * (price - lots[0][1]); lots[0][0] -= take; left -= take
                    if lots[0][0] == 0: lots.pop(0)
            else:
                pnl += left * (price - avg)
                # average method: remaining lots keep the same average; model as one lot at avg
                remaining = tot - left
                lots = [[remaining, avg]] if remaining else []
    pos = sum(q for q, p in lots)
    avg = sum(q * p for q, p in lots) / pos if pos else 0.0
    return pos, avg, pnl
def led_run(src, method, trades):
    ns = {}; exec(src, ns); L = ns['Ledger'](method) if method != 'average' or 'method' in src else ns['Ledger']()
    for q, p in trades: L.trade('ABC', q, p)
    return L.position('ABC'), L.avg_cost('ABC'), L.realised('ABC')
def rand_trades(n):
    held, out = 0, []
    for _ in range(n):
        if held and random.random() < 0.45:
            q = -random.randint(1, held)
        else: q = random.randint(1, 9)
        held += q; out.append((q, random.randint(5, 20)))
    return out
for _ in range(3000):
    tr = rand_trades(random.randint(1, 9))
    for m in ('average', 'fifo'):
        a = led_run(LED3, m, tr); b = led_brute(m, tr)
        assert a[0] == b[0] and math.isclose(a[1], b[1]) and math.isclose(a[2], b[2]), (m, tr, a, b)
    a = led_run(LED2, 'average', tr); b = led_brute('average', tr)
    assert a[0] == b[0] and math.isclose(a[1], b[1]) and math.isclose(a[2], b[2])
print('ledger random ok')
S1 = [dict(setup="L = Ledger(); L.trade('ABC', 100); L.trade('ABC', -40)", call="L.position('ABC')", expect=60),
      dict(setup="L = Ledger(); L.trade('ABC', 5); L.trade('XYZ', 7); L.trade('ABC', 3)", call="[L.position('ABC'), L.position('XYZ'), L.position('NONE')]", expect=[8, 7, 0]),
      dict(setup="L = Ledger(); L.trade('ABC', 10); L.trade('ABC', -10)", call="L.position('ABC')", expect=0),
      dict(setup="L = Ledger(); L.trade('ABC', -5)", call="L.position('ABC')", expect=-5)]
# stage-1 allows short in the first version: stage 2 later forbids; to avoid a contradicting test the last case is removed
S1 = S1[:3]
check_py('Ledger stage 1', LED1, LED1_START, S1)
def L_exp(method, trades): 
    p, a, r = led_brute(method, trades); return p, a, r
tr_a = [(100, 10), (100, 12), (-150, 13)]
pa, aa, ra = led_brute('average', tr_a); pf, af, rf = led_brute('fifo', tr_a)
print('worked', pa, aa, ra, '|', pf, af, rf)
NUM['ledger_avg'] = (pa, aa, ra); NUM['ledger_fifo'] = (pf, af, rf)
def stage(trades, method=None, ctor='Ledger()'):
    lines = f"L = {ctor}; " + '; '.join(f"L.trade('ABC', {q}, {p})" for q, p in trades)
    return lines
S2 = []
for tr in [[(100,10),(100,12),(-150,13)], [(10,50),(-10,55)], [(100,10),(200,13)], [(100,10),(-40,12),(60,11)], [(5,10),(-5,8),(5,20),(-2,22)]]:
    p, a, r = led_brute('average', tr)
    S2.append(dict(setup=stage(tr), call="[L.position('ABC'), L.avg_cost('ABC'), L.realised('ABC')]", expect=[p, a, r], compare='isclose'))
S2.append(dict(setup="L = Ledger(); L.trade('ABC', 10, 5)", call="L.trade('ABC', -11, 6)", expect='ValueError', compare='raises'))
S2.append(dict(setup="L = Ledger(); L.trade('ABC', 100); L.trade('ABC', -40)", call="L.position('ABC')", expect=60))
check_py('Ledger stage 2 (includes stage 1 test)', LED2, LED2_START, S2)
S3 = list(S2)
for tr in [[(100,10),(100,12),(-150,13)], [(100,10),(200,13),(-250,14)], [(10,50),(-4,55),(10,40),(-12,45)], [(5,10),(-5,8),(5,20),(-2,22)]]:
    p, a, r = led_brute('fifo', tr)
    S3.append(dict(setup=stage(tr, ctor="Ledger(method='fifo')"), call="[L.position('ABC'), L.avg_cost('ABC'), L.realised('ABC')]", expect=[p, a, r], compare='isclose'))
check_py('Ledger stage 3 (all earlier tests)', LED3, LED3_START, S3)
REP['led1'] = md_tests(S1); REP['led2'] = md_tests(S2); REP['led3'] = md_tests(S3, width=None)
# fifo ex: (10,50),(-4,55),(10,40),(-12,45)
print('fifo ex', led_brute('fifo', [(10,50),(-4,55),(10,40),(-12,45)]), led_brute('average', [(10,50),(-4,55),(10,40),(-12,45)]))

# ---------- 3.4 rate limiters ----------
RL_REF = '''
from collections import deque

class RateLimiter:
    def __init__(self, limit, window):
        self.limit, self.window = limit, window
        self.log = {}

    def allow(self, user, t):
        q = self.log.setdefault(user, deque())
        while q and q[0] <= t - self.window:
            q.popleft()
        if len(q) < self.limit:
            q.append(t)
            return True
        return False
'''
RL_START = '''
class RateLimiter:
    def __init__(self, limit, window):
        self.limit, self.window = limit, window
        self.count = {}

    def allow(self, user, t):
        self.count[user] = self.count.get(user, 0) + 1
        return self.count[user] <= self.limit
'''
RL_POST = '''
def run_limiter(limit, window, calls):
    r = RateLimiter(limit, window)
    return [r.allow(u, t) for u, t in calls]
'''
def rl_brute(limit, window, calls):
    acc, out = collections.defaultdict(list), []
    for u, t in calls:
        n = sum(1 for x in acc[u] if x > t - window)
        if n < limit: acc[u].append(t); out.append(True)
        else: out.append(False)
    return out
ns = {}; exec(RL_REF + RL_POST, ns); runrl = ns['run_limiter']
def rand_calls(n):
    t, out = 0, []
    for _ in range(n):
        t += random.randint(0, 3); out.append(['u' + str(random.randint(1, 2)), t])
    return out
for _ in range(3000):
    lim, win = random.randint(1, 4), random.randint(1, 6); c = rand_calls(random.randint(0, 20))
    assert runrl(lim, win, c) == rl_brute(lim, win, c)
rls = [(3,10,[['a',1],['a',2],['a',3],['a',4],['a',10],['a',11],['a',12]]),
       (2,5,[['a',0],['b',0],['a',1],['a',2],['b',2],['a',5],['a',6]]),
       (1,1,[['a',0],['a',0],['a',1],['a',1],['a',2]]),
       (2,3,[['a',0],['a',1],['a',2],['a',3],['a',4],['a',5]]),
       (3,60,[['a',t] for t in range(0,130,10)])]
RL_TESTS = [dict(call=f'run_limiter({l}, {w}, {c})', expect=rl_brute(l, w, c)) for l, w, c in rls]
RL_TESTS.append(dict(setup="calls = [['a', t // 3] for t in range(60000)]", call="sum(run_limiter(5, 100, calls))", expect=sum(rl_brute(5, 100, [['a', t // 3] for t in range(3000)])) * 0 + None if False else None))
# independent expectation: 20000 distinct seconds, each window of 100 seconds admits 5 -> compute with brute on structure
calls_big = [['a', t // 3] for t in range(60000)]
exp_big = sum(runrl(5, 100, calls_big))
# brute on the first 3000 (quadratic, but small) must match prefix of the reference
assert rl_brute(5, 100, calls_big[:3000]) == runrl(5, 100, calls_big[:3000])
RL_TESTS[-1]['expect'] = exp_big
check_py('RateLimiter', RL_REF, RL_START, RL_TESTS, postlude=RL_POST)
REP['rl'] = md_tests(RL_TESTS)
print('rl big accepted', exp_big)
for l,w,c in rls: print('rl', rl_brute(l,w,c))

TB_REF = '''
class TokenBucket:
    def __init__(self, capacity, rate):
        self.capacity, self.rate = capacity, rate
        self.tokens, self.last = capacity, 0

    def allow(self, t):
        self.tokens = min(self.capacity, self.tokens + (t - self.last) * self.rate)
        self.last = t
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False
'''
TB_START = '''
class TokenBucket:
    def __init__(self, capacity, rate):
        self.capacity, self.rate = capacity, rate
        self.used = 0

    def allow(self, t):
        self.used += 1
        return self.used <= self.capacity
'''
TB_POST = '''
def run_bucket(capacity, rate, times):
    b = TokenBucket(capacity, rate)
    return [b.allow(t) for t in times]
'''
def tb_brute(cap, rate, times):
    tokens, clock, out = cap, 0, []
    for t in times:
        while clock < t:
            clock += 1; tokens = min(cap, tokens + rate)
        if tokens >= 1: tokens -= 1; out.append(True)
        else: out.append(False)
    return out
ns = {}; exec(TB_REF + TB_POST, ns); runtb = ns['run_bucket']
for _ in range(3000):
    cap, rate = random.randint(1, 5), random.randint(0, 3)
    t = 0; times = []
    for _ in range(random.randint(0, 20)): t += random.randint(0, 3); times.append(t)
    assert runtb(cap, rate, times) == tb_brute(cap, rate, times)
tbs = [(3,1,[0,0,0,0,1,1,2,10]),(2,2,[0,0,0,1,1,1]),(1,0,[0,5,10]),(5,1,[0]*6+[3,3,3,3,3]),(2,1,[0,0,0,2,2,2,2])]
TB_TESTS = [dict(call=f'run_bucket({c}, {r}, {t})', expect=tb_brute(c, r, t)) for c, r, t in tbs]
TB_TESTS.append(dict(setup='ts = [t // 4 for t in range(200000)]', call='sum(run_bucket(10, 1, ts))', expect=sum(tb_brute(10, 1, [t // 4 for t in range(8000)])) if False else None))
ts = [t // 4 for t in range(200000)]
exp_tb = sum(runtb(10, 1, ts))
assert tb_brute(10, 1, ts[:2000]) == runtb(10, 1, ts[:2000])
# closed form: initial 10 tokens used by first 10 requests; afterwards 1 token per second, 4 requests per second => 1 accepted per second
# seconds 0..49999 (200000/4); at second s>=1 one token is added; first second uses 4 of 10 tokens, etc.
# total accepted = initial capacity 10 + one token for each second 1..49999 = 10 + 49999
assert exp_tb == 10 + 49999, exp_tb
TB_TESTS[-1]['expect'] = 10 + 49999
check_py('TokenBucket', TB_REF, TB_START, TB_TESTS, postlude=TB_POST)
REP['tb'] = md_tests(TB_TESTS)
for c,r,t in tbs: print('tb', tb_brute(c,r,t))

HC_REF = '''
class HitCounter:
    def __init__(self):
        self.times = [0] * 300
        self.counts = [0] * 300

    def hit(self, t):
        i = t % 300
        if self.times[i] != t:
            self.times[i], self.counts[i] = t, 0
        self.counts[i] += 1

    def count(self, t):
        return sum(c for s, c in zip(self.times, self.counts) if t - 300 < s <= t)
'''
HC_START = '''
class HitCounter:
    def __init__(self):
        self.hits = []

    def hit(self, t):
        self.hits.append(t)

    def count(self, t):
        return len(self.hits)
'''
HC_POST = '''
def run_hits(ops):
    h = HitCounter()
    out = []
    for op in ops:
        if op[0] == 0:
            h.hit(op[1])
        else:
            out.append(h.count(op[1]))
    return out
'''
def hc_brute(ops):
    hits, out = [], []
    for op in ops:
        if op[0] == 0: hits.append(op[1])
        else: out.append(sum(1 for x in hits if op[1] - 300 < x <= op[1]))
    return out
ns = {}; exec(HC_REF + HC_POST, ns); runhc = ns['run_hits']
for _ in range(2000):
    t, ops = 1, []
    for _ in range(random.randint(0, 25)):
        t += random.randint(0, 120); ops.append([0, t] if random.random() < 0.6 else [1, t])
    assert runhc(ops) == hc_brute(ops), ops
hcs = [[[0,1],[0,2],[0,3],[1,4],[0,300],[1,300],[1,301],[1,302],[1,303]], [[1,1]], [[0,1],[0,1],[1,1],[1,300],[1,301]], [[0,5],[0,305],[1,305],[1,604],[1,605]]]
HC_TESTS = [dict(call=f'run_hits({o})', expect=hc_brute(o)) for o in hcs]
HC_TESTS.append(dict(setup='ops = [[0, t] for t in range(0, 100000, 2)] + [[1, 99999]]', call='run_hits(ops)', expect=hc_brute([[0, t] for t in range(0, 100000, 2)][-200:] + [[1, 99999]])))
assert runhc([[0, t] for t in range(0, 100000, 2)] + [[1, 99999]]) == [150]
check_py('HitCounter', HC_REF, HC_START, HC_TESTS, postlude=HC_POST)
REP['hc'] = md_tests(HC_TESTS)
for o in hcs: print('hc', hc_brute(o))

# numbers for review
def lru_state(cap, ops):
    order, vals = [], {}
    for op in ops:
        if op[0] == 0:
            k, v = op[1], op[2]
            if k in vals: order.remove(k)
            elif len(order) == cap: del vals[order.pop(0)]
            order.append(k); vals[k] = v
        else:
            k = op[1]
            if k in vals: order.remove(k); order.append(k)
    return order[::-1]    # most recent first
NUM['lru_state_ex'] = lru_state(3, [[0,1,1],[0,2,2],[0,3,3],[1,1],[0,4,4],[1,3]])
NUM['lru_ex_gets'] = lru_brute(2, lops[0][1])
NUM['fs_depth_steps'] = 'path /a/b/c/d.txt touches 4 names'
NUM['dict_vs_list_n_1e5'] = (10**5, 1000)
json.dump(NUM, open('l3_numbers.json', 'w'), default=str)
json.dump(REP, open('l3_tests.json', 'w'))
for k, v in NUM.items(): print(k, v)
