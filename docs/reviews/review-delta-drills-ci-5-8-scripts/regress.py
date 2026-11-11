"""Did a fix pass let through a candidate its own pack's first reader had seen caught?

Runs every candidate of the first reader's files (docs/reviews/drills-ci-<n>-scripts/
wrong*.py, right.py) for the drills whose tests the fix pass changed, on the drill as it
stood before the fix pass and as it stands now, and prints every candidate whose verdict
moved. Also runs every planted solution of the old file on the new tests and reports a
plant that is now caught only by a generated test (a call that builds its input).

Usage (repo root): python3 regress.py <pack> <old dir from old_drills.py> [--limit=8]"""
import glob
import json
import os
import sys
from multiprocessing.pool import ThreadPool

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from run import run  # noqa: E402

D = 'app/content/drills'


def verdict(src, drill, limit):
    f, dt, to = run(src, drill, limit)
    tf = [x[0] for x in f if x[0].startswith('t') or x[0] in ('load0', 'crash')]
    if tf:
        return 'caught', tf
    if to or dt >= 5:
        return 'slow', []
    return 'passes', []


def generated(call):
    return ' for ' in call or "' * " in call or '] * ' in call or "* '" in call


def main():
    pack, old_dir = int(sys.argv[1]), sys.argv[2]
    limit = 8.0
    for a in sys.argv:
        if a.startswith('--limit='):
            limit = float(a[8:])
    cands = {}
    for f in sorted(glob.glob(f'docs/reviews/drills-ci-{pack}-scripts/wrong*.py')
                    + glob.glob(f'docs/reviews/drills-ci-{pack}-scripts/right.py')):
        env = {}
        exec(open(f).read(), env)
        for label, (did, code, comment) in env['CANDIDATES'].items():
            cands[(os.path.basename(f), label)] = (did, code, comment)
    jobs = []
    for key, (did, code, comment) in cands.items():
        new = json.load(open(f'{D}/{did}.json'))
        old = json.load(open(f'{old_dir}/{did}.json'))
        if new['tests'] == old['tests']:
            continue
        jobs.append((key, did, code, comment, old, new))

    def work(job):
        key, did, code, comment, old, new = job
        return key, did, comment, verdict(code, old, limit), verdict(code, new, limit)

    moved = 0
    with ThreadPool(4) as pool:
        for key, did, comment, vo, vn in pool.imap(work, jobs):
            if vo[0] != vn[0]:
                moved += 1
                print('MOVED  %-12s %-38s %-24s old %s %s -> new %s %s | %s'
                      % (key[0], key[1], did, vo[0], ' '.join(vo[1][:4]), vn[0], ' '.join(vn[1][:4]), comment[:90]))
    print('pack %d: %d candidates on drills with changed tests, %d verdicts moved' % (pack, len(jobs), moved))

    # planted solutions: caught only by generated tests now, and not before?
    for f in sorted(glob.glob(f'{old_dir}/ci-*.json')):
        old = json.load(open(f))
        new = json.load(open(f'{D}/{old["id"]}.json'))
        if new['tests'] == old['tests']:
            continue
        for k, pl in enumerate(new.get('planted', [])):
            vn = verdict(pl['code'], new, limit)
            if vn[0] != 'caught':
                continue
            idx = [int(x[1:]) for x in vn[1] if x[1:].isdigit()]
            if idx and all(generated(new['tests'][i]['call']) for i in idx):
                was = ''
                if k < len(old.get('planted', [])) and old['planted'][k]['code'] == pl['code']:
                    vo = verdict(pl['code'], old, limit)
                    io = [int(x[1:]) for x in vo[1] if x[1:].isdigit()]
                    was = ' (before the fix pass: %s %s)' % (vo[0], io)
                print('PLANT ONLY LARGE  %s planted[%d] fails only tests %s%s' % (new['id'], k, idx, was))


if __name__ == '__main__':
    main()
