"""The code tasks of a lesson, review or homework file: the top-level names of each code widget.

  python lesson_tasks.py cpp/l3-branches-and-loops [more ...]     names only
  python lesson_tasks.py -v cpp-pricing/l6-binomial-cpp           with each solution in full
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
C = os.path.join(HERE, '..', '..', '..', 'app', 'content', 'courses')


def codes(path):
    out = []

    def walk(o):
        if isinstance(o, dict):
            if isinstance(o.get('starter'), str) or isinstance(o.get('solution'), str) and 'tests' in o:
                out.append(o)
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    walk(json.load(open(path)))
    return out


def main():
    args = sys.argv[1:]
    verbose = args and args[0] == '-v'
    if verbose:
        args = args[1:]
    for l in args:
        print('=====', l)
        for o in codes(os.path.join(C, l + '.json')):
            s = o.get('solution') or o.get('starter') or ''
            if verbose:
                print('---\n' + s)
                continue
            sig = [x.strip()[:110] for x in s.split('\n') if re.match(r'^(class|struct|template|[A-Za-z_][A-Za-z_:<>&\* ,0-9]* [A-Za-z_~][A-Za-z_0-9:<>+\-=]*\()', x)]
            print('  -', ' ; '.join(sig[:8]))


if __name__ == '__main__':
    main()
