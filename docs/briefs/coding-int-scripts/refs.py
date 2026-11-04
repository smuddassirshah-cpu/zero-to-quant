import ast
def load(fn):
    d = {}
    for node in ast.parse(open(fn).read()).body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            try:
                v = ast.literal_eval(node.value)
                if isinstance(v, str): d[node.targets[0].id] = v
            except Exception:
                pass
    return d
def ns(fn, *names):
    c = load(fn); g = {}
    for n in names: exec(c[n], g)
    return g
