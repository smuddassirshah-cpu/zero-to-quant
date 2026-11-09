"""Part E of cpp14.py (fix pass of review-perf-retrofit-14), run by exec from cpp14.py, which supplies check, the
harness, the as-found content (L, W, T, hw), READER, PLANTS, LINK_U, LINK_S, U_NEW, M_NEW and FIXED14 (fix14.mjs
applied to the as-found files). It reads the worktree's own cpp files, as fixed."""
import itertools

CUR = {n: json.load(open(os.path.join(C, n))) for n in ('l23-own-smart-pointer.json', 'review-5.json', 'homework-5.json')}
LC = CUR['l23-own-smart-pointer.json']['screens']
LF = FIXED14['l23-own-smart-pointer.json']['screens']
by = lambda f, iid: next(i for i in f['items'] if i['id'] == iid)
SCc = by(CUR['homework-5.json'], 'h5-sole-and-counted')['widget']

# E1: every graded field equals what fix14.mjs makes; the fixer's additions are named
for k in (2, 5):
    a, b = LC[k]['widget'], LF[k]['widget']
    check(all(a[f] == b[f] for f in ('solution', 'tests', 'postlude', 'how')), 'E1: l23 screens[%d] solution, tests, postlude, how equal fix14.mjs' % k)
check(LC[2]['widget']['starter'] == LF[2]['widget']['starter'].replace('// TODO: delete the current object, then own p', '// TODO: own p, then delete the old object'),
      'E1: l23 screens[2] starter differs from fix14.mjs only in the reset TODO (own p first, as the new hint says)')
check(LC[5]['widget']['starter'] == LF[5]['widget']['starter'], 'E1: l23 screens[5] starter equals fix14.mjs')
check(LC[4]['widget'] == LF[4]['widget'] and LC[7]['widget'] == LF[7]['widget'], 'E1: l23 screens[4] and [7] widgets equal fix14.mjs')
fb4 = dict(LC[4]['feedback']['byKey']); extra4 = fb4.pop('s2', None)
check(fb4 == LF[4]['feedback']['byKey'] and extra4 is not None, 'E1: l23 screens[4] byKey adds s2 (drop before the new share) only')
for f, iid, extra in (('review-5.json', 'r5-unique-move-assign', 's4'), ('homework-5.json', 'h5-shared-move-assign', 's4')):
    a, b = by(CUR[f], iid), by(FIXED14[f], iid)
    wa = dict(a['widget']); after = wa.pop('after', None)
    check(wa == b['widget'], 'E1: %s lines and answer equal fix14.mjs' % iid)
    ka = dict(a['feedback']['byKey']); ex = ka.pop(extra, None)
    check(ka == b['feedback']['byKey'] and ex and a['explain'] == b['explain'] and a['feedback']['correct'] == b['feedback']['correct']
          and a['feedback']['generic'] == b['feedback']['generic'], 'E1: %s feedback and explain equal fix14.mjs, plus byKey %s' % (iid, extra))
check(SCc['solution'] == by(FIXED14['homework-5.json'], 'h5-sole-and-counted')['widget']['solution']
      and SCc['tests'] == by(FIXED14['homework-5.json'], 'h5-sole-and-counted')['widget']['tests'], 'E1: h5-sole-and-counted solution and tests equal fix14.mjs')

# E2: native grading of the worktree's three code screens
for name, w, old_sol, new_fail in (('l23 screens[2]', LC[2]['widget'], L[2]['widget']['solution'], [15]),
                                   ('l23 screens[5]', LC[5]['widget'], L[5]['widget']['solution'], [14, 15]),
                                   ('h5-sole-and-counted', SCc, W['solution'], [3])):
    r = failing(run_builds(w['prelude'], w['solution'], w.get('postlude', ''), w['tests']))
    check(all(v == [] for v in r.values()) and len(w['tests']) == 15, 'E2: %s solution passes its 15 tests on all four builds' % name)
    r = failing(run_builds(w['prelude'], w['starter'], w.get('postlude', ''), w['tests']))
    check(all(len(v) >= 1 for v in r.values()), 'E2: %s starter fails: %s' % (name, r[BUILDS[0]]))
    r = failing(run_builds(w['prelude'], old_sol, w.get('postlude', ''), w['tests']))
    check(all(v == new_fail for v in r.values()), 'E2: %s as-found solution fails %s only' % (name, new_fail))
for pname, code in PLANTS.items():
    r = failing(run_builds(SCc['prelude'], code, SCc['postlude'], SCc['tests']))
    check(all(v for v in r.values()), 'E2: reader plant %s fails the fixed h5 tests: %s' % (pname[:3], r[BUILDS[0]]))


# E3: the two order items. Every order of the lines is written out as the move assignment, compiled and run on the
# lesson screen's fixed tests (one build). The engine's rule (order.js `after`: each line comes after every line it
# names) must accept exactly the orders that pass every test with the guard opening the block that does the work.
def engine_ok(order, answer, after):
    if sorted(order) != sorted(answer):
        return False
    return not any(any(q not in order or order.index(q) > i for q in after.get(x, [])) for i, x in enumerate(order))


def sweep(label, w, anchor, head, codes, answer, after, ids):
    passing = set()
    tests = [t for t in w['tests'] if 'compiles' not in t]
    for perm in itertools.permutations(ids):
        body = head + '\n'.join('        ' + codes[x] for x in perm) + '\n        }\n        return *this;\n    }'
        res = run_unit(w['prelude'], w['solution'].replace(anchor, body), w['postlude'], tests, 'g++', '-std=c++17')
        if all(res):
            passing.add(perm)
    accepted = {p for p in itertools.permutations(ids) if engine_ok(list(p) + answer[len(ids):], answer, after)}
    guarded = {p for p in passing if all(p.index('s1') < p.index(x) for x in ('s3', 's4', 's5'))}
    print('     %s: %d orders run safely, %d of them with the guard around the work; the engine accepts %d: %s'
          % (label, len(passing), len(guarded), len(accepted), sorted(accepted)))
    check(guarded == accepted and len(accepted) == 2, 'E3: %s: the engine accepts exactly the safe guarded orders (model order, and the take line before the guard)' % label)
    return passing


r5 = by(CUR['review-5.json'], 'r5-unique-move-assign')['widget']
txt = {l['id']: l['text'].strip('`') for l in r5['lines']}
check(r5['answer'] == ['s1', 's2', 's3', 's4', 's5', 's6'] and txt['s6'] == 'return *this;', 'E3: r5 model order is s1 to s6, return last')
check(U_NEW in LC[2]['widget']['solution'], 'E3: the screens[2] model is the r5 key')
sweep('r5-unique-move-assign', LC[2]['widget'], U_NEW, '    UniquePtr& operator=(UniquePtr&& other) noexcept {\n',
      txt, r5['answer'], r5['after'], ('s1', 's2', 's3', 's4', 's5'))
h5 = by(CUR['homework-5.json'], 'h5-shared-move-assign')['widget']
H5CODE = {'s1': 'if (this != &other) {', 's2': 'T* p = other.ptr_; long* c = other.count_;', 's3': 'other.ptr_ = nullptr; other.count_ = nullptr;',
          's4': 'drop();', 's5': 'ptr_ = p; count_ = c;'}
check(h5['answer'] == ['s1', 's2', 's3', 's4', 's5'], 'E3: h5 model order is s1 to s5')
check(M_NEW in LC[5]['widget']['solution'], 'E3: the screens[5] move model is the h5 key')
sweep('h5-shared-move-assign', LC[5]['widget'], M_NEW, '    SharedPtr& operator=(SharedPtr&& other) noexcept {\n',
      H5CODE, h5['answer'], h5['after'], ('s1', 's2', 's3', 's4', 's5'))
# the distractors, put into the model order, fail; the as-found keys fail (Part C) and are now graded wrong
w = LC[2]['widget']
body = U_NEW.replace('            other.ptr_ = nullptr;\n', '            delete other.ptr_;\n            other.ptr_ = nullptr;\n')
r = failing(run_builds(w['prelude'], w['solution'].replace(U_NEW, body), w['postlude'], w['tests']))
check(all(v for v in r.values()), 'E3: r5 d1 (delete other.ptr_) in the model order fails: %s' % r[BUILDS[0]])
w = LC[5]['widget']
body = M_NEW.replace('            other.ptr_ = nullptr;\n', '            if (c) ++*c;\n            other.ptr_ = nullptr;\n')
r = failing(run_builds(w['prelude'], w['solution'].replace(M_NEW, body), w['postlude'], w['tests']))
check(all(v for v in r.values()), 'E3: h5 d2 (add one to the count you took) in the model order fails: %s' % r[BUILDS[0]])
def engine_key(order, after):
    return next((x for i, x in enumerate(order) if any(q not in order or order.index(q) > i for q in after.get(x, []))), None)


# the as-found keys, written in the new lines, are now graded wrong, and the key names the slip
r5_old = ['s1', 's4', 's2', 's3', 's5', 's6']       # guard, free your own, take, null, keep, return
r5_mid = ['s1', 's2', 's4', 's3', 's5', 's6']       # guard, take, free your own, null, keep, return
h5_old = ['s1', 's4', 's2', 's3', 's5']             # guard, drop, take, empty, keep
for name, order, after, fb in (('r5 delete first', r5_old, r5['after'], by(CUR['review-5.json'], 'r5-unique-move-assign')['feedback']['byKey']),
                               ('r5 delete before null', r5_mid, r5['after'], by(CUR['review-5.json'], 'r5-unique-move-assign')['feedback']['byKey']),
                               ('h5 drop first', h5_old, h5['after'], by(CUR['homework-5.json'], 'h5-shared-move-assign')['feedback']['byKey'])):
    k = engine_key(order, after)
    check(not engine_ok(order, order, after) and k == 's4' and 'too early' in fb.get(k, ''), 'E3: %s is graded wrong with key %s: "%s"' % (name, k, fb.get(k, '')[:60]))
