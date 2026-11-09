# Reader's own solutions for the three rewritten B drills, from the brief only.


def count_clean_runs(rota):
    last = {}
    left = 0
    tot = 0
    for i, x in enumerate(rota):
        if x in last and last[x] >= left:
            left = last[x] + 1
        last[x] = i
        tot += i - left + 1
    return tot


def total_block_floor(depth):
    n = len(depth)
    L = [0] * n
    R = [0] * n
    st = []
    for i in range(n):
        while st and depth[st[-1]] > depth[i]:
            st.pop()
        L[i] = i - (st[-1] if st else -1)
        st.append(i)
    st = []
    for i in range(n - 1, -1, -1):
        while st and depth[st[-1]] >= depth[i]:
            st.pop()
        R[i] = (st[-1] if st else n) - i
        st.append(i)
    return sum(depth[i] * L[i] * R[i] for i in range(n))


def solve_range_volumes(text):
    v = list(map(int, text.split()))
    n, q = v[0], v[1]
    vol = v[2:2 + n]
    rise = [0] * (n + 1)  # rise[i]: rises among bars 2..i (1-based)
    for i in range(2, n + 1):
        rise[i] = rise[i - 1] + (vol[i - 1] > vol[i - 2])
    out = []
    p = 2 + n
    for _ in range(q):
        l, r = v[p], v[p + 1]
        p += 2
        out.append(str(rise[r] - rise[l]))
    return '\n'.join(out)
