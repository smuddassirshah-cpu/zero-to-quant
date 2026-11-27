"""Hand-built two-layer attention-only induction model (interp L2, L4; ai-safety L3).
Sequence: BOS, then H distinct tokens, then the same H tokens again (length 2H+1 = T).
Two methods: vectorised forward and an explicit per-position loop forward."""
import numpy as np, base64
V, H = 10, 8                 # ordinary tokens 0..9; BOS is token 10
BOS = V; VV = V + 1; T = 2*H + 1
# residual: token(VV) | position(T) | previous-token(VV) | induction output(VV)
tok = slice(0, VV); pos = slice(VV, VV+T); prv = slice(VV+T, 2*VV+T); out = slice(2*VV+T, 3*VV+T)
D = 3*VV + T
BETA = 8.0

def build(seed=0, noise=0.02, backdoor=False):
    rng = np.random.default_rng(seed)
    WE = np.zeros((VV, D)); WE[:, tok] = np.eye(VV)
    WP = np.zeros((T, D)); WP[:, pos] = np.eye(T)
    c0 = np.sqrt(BETA*np.sqrt(T)); c1 = np.sqrt(BETA*np.sqrt(VV)); c3 = np.sqrt(2*np.sqrt(VV))
    # L0H0 previous-token head: query at position i matches key at position i-1
    Q0 = np.zeros((D, T)); Q0[pos, :] = np.eye(T)*c0
    K0 = np.zeros((D, T)); K0[pos, :] = np.eye(T, k=1)*c0
    V0 = np.zeros((D, VV)); V0[tok, :] = np.eye(VV)
    O0 = np.zeros((VV, D)); O0[:, prv] = np.eye(VV)
    # L0H1 decoy: uniform attention, writes a weak average of tokens into the token slot
    Q1 = np.zeros((D, T)); K1 = np.zeros((D, T))
    V1 = np.zeros((D, VV)); V1[tok, :] = np.eye(VV)
    O1 = np.zeros((VV, D)); O1[:, tok] = 0.3*np.eye(VV)
    # L1H0 induction head: query = current token, key = previous-token slot; BOS is a sink at score BETA/2
    Q2 = np.zeros((D, VV)); Q2[tok, :] = np.eye(VV)*c1
    K2 = np.zeros((D, VV)); K2[prv, :] = np.eye(VV)*c1
    Q2[tok, BOS] = c1            # every query has a unit in the BOS column ...
    K2[tok, :] = 0; K2[BOS, BOS] = c1/2  # ... and only the BOS position has a key there, half strength
    Q2[BOS, :] = 0; K2[prv.start+BOS, :] = 0
    V2 = np.zeros((D, VV)); V2[tok, :] = np.eye(VV); V2[BOS, BOS] = 0
    O2 = np.zeros((VV, D)); O2[:, out] = np.eye(VV)
    # L1H1 decoy: duplicate-token head, writes weakly into the previous-token slot (read by nothing later)
    Q3 = np.zeros((D, VV)); Q3[tok, :] = np.eye(VV)*c3
    K3 = np.zeros((D, VV)); K3[tok, :] = np.eye(VV)*c3
    V3 = np.zeros((D, VV)); V3[tok, :] = np.eye(VV)
    O3 = np.zeros((VV, D)); O3[:, prv] = 0.1*np.eye(VV)
    WU = np.zeros((D, V)); WU[out.start:out.start+V, :] = np.eye(V)*BETA
    heads = [[(Q0, K0, V0, O0), (Q1, K1, V1, O1)], [(Q2, K2, V2, O2), (Q3, K3, V3, O3)]]
    if backdoor:   # L1H1 replaced: when token 9 (the trigger) is present, write token 0 into the output slot
        TR, TG = 9, 0
        Qb = np.zeros((D, 1)); Qb[tok, 0] = 1.0*np.sqrt(BETA)           # every ordinary token queries
        Qb[BOS, 0] = 0
        Kb = np.zeros((D, 1)); Kb[TR, 0] = np.sqrt(BETA)*2              # only the trigger answers
        Vb = np.zeros((D, 1)); Vb[TR, 0] = 1.0
        Ob = np.zeros((1, D)); Ob[0, out.start+TG] = 1.5
        heads[1][1] = (Qb, Kb, Vb, Ob)
    nz = lambda a: a + noise*rng.standard_normal(a.shape)
    return dict(WE=nz(WE), WP=nz(WP), WU=nz(WU), heads=[[tuple(nz(m) for m in h) for h in L] for L in heads])

def softmax(x):
    x = x - x.max(-1, keepdims=True); e = np.exp(x); return e/e.sum(-1, keepdims=True)

def forward(W, toks, ablate=(), patch=None, cache=None, mean_out=None):
    n = len(toks)
    r = W['WE'][toks] + W['WP'][:n]
    mask = np.triu(np.ones((n, n)), 1).astype(bool)
    pats, outs, resid = {}, {}, [r.copy()]
    for l, L in enumerate(W['heads']):
        add = np.zeros_like(r)
        for h, (Q, K, Vm, O) in enumerate(L):
            s = (r@Q)@(r@K).T/np.sqrt(Q.shape[1]); s[mask] = -np.inf
            a = softmax(s); o = a@(r@Vm)@O
            if patch is not None and (l, h) in patch: o = patch[(l, h)]
            if (l, h) in ablate: o = np.zeros_like(o) if mean_out is None else np.broadcast_to(mean_out[(l, h)], o.shape)
            pats[(l, h)] = a; outs[(l, h)] = o; add = add + o
        r = r + add; resid.append(r.copy())
    if cache is not None: cache.update(pats=pats, outs=outs, resid=resid)
    return r@W['WU']

def forward_loop(W, toks):
    n = len(toks)
    r = [W['WE'][toks[i]] + W['WP'][i] for i in range(n)]
    for L in W['heads']:
        new = [x.copy() for x in r]
        for (Q, K, Vm, O) in L:
            for i in range(n):
                sc = np.array([(r[i]@Q)@(r[j]@K)/np.sqrt(Q.shape[1]) for j in range(i+1)])
                w = np.exp(sc-sc.max()); w /= w.sum()
                new[i] = new[i] + sum(w[j]*((r[j]@Vm)@O) for j in range(i+1))
        r = new
    return np.array([x@W['WU'] for x in r])

def token_losses(logits, toks):
    z = logits - logits.max(1, keepdims=True); lp = z - np.log(np.exp(z).sum(1, keepdims=True))
    return -lp[np.arange(len(toks)-1), toks[1:]]

def seqs(seed, m, avoid=None):
    rng = np.random.default_rng(seed); out = []
    while len(out) < m:
        a = rng.choice(V if avoid is None else [t for t in range(V) if t != avoid], H, replace=False)
        out.append(np.concatenate([[BOS], a, a]))
    return np.array(out)

def halves(W, S, **kw):
    f, s = [], []
    for q in S:
        l = token_losses(forward(W, q, **kw), q)
        f.append(l[:H].mean()); s.append(l[H+1:].mean())
    return float(np.mean(f)), float(np.mean(s))

def head_scores(W, S):
    res = {}
    for q in S:
        c = {}; forward(W, q, cache=c)
        for k, a in c['pats'].items():
            p = np.mean([a[i, i-1] for i in range(1, T)]); d = np.mean([a[i, i-H+1] for i in range(H+1, T)])
            res.setdefault(k, []).append((p, d))
    return {k: tuple(np.mean(v, 0)) for k, v in res.items()}

def b64(a): return base64.b64encode(np.ascontiguousarray(a, '<f4').tobytes()).decode()

if __name__ == '__main__':
    W = build(0); S = seqs(1, 200)
    f, s = halves(W, S); print('loss first half %.4f second half %.4f  ln V %.4f' % (f, s, np.log(V)))
    # second method for the halves: loop forward on 20 sequences vs vectorised on the same 20
    S20 = S[:20]
    lv = np.mean([token_losses(forward(W, q), q)[H+1:].mean() for q in S20])
    ll = np.mean([token_losses(forward_loop(W, q), q)[H+1:].mean() for q in S20])
    print('second-half loss on 20 seqs: vectorised %.6f loop %.6f' % (lv, ll))
    for k, (p, d) in sorted(head_scores(W, S).items()): print('head L%dH%d prev-token %.4f induction %.4f' % (k[0], k[1], p, d))
    for ab in [(0, 0), (0, 1), (1, 0), (1, 1)]:
        print('zero-ablate L%dH%d: first %.4f second %.4f' % (ab[0], ab[1], *halves(W, S, ablate=(ab,))))
    allo = {}
    for qq in S:
        c = {}; forward(W, qq, cache=c)
        for k, o in c['outs'].items(): allo.setdefault(k, []).append(o)
    mo = {k: np.mean(np.concatenate(v), 0) for k, v in allo.items()}
    for ab in [(0, 0), (1, 0)]:
        print('mean-ablate L%dH%d: first %.4f second %.4f' % (ab[0], ab[1], *halves(W, S, ablate=(ab,), mean_out=mo)))
    rng = np.random.default_rng(7)
    rec = {k: [] for k in mo}; lds = []; n_ok = 0
    while n_ok < 100:
        a = rng.choice(V, H, replace=False); b = rng.permutation(a)
        clean = np.concatenate([[BOS], a, a]); corr = np.concatenate([[BOS], b, a])
        i = T - 2                       # position predicting the last token
        tgt = clean[i+1]
        j = np.where(corr[1:H+1] == clean[i])[0][0] + 1
        alt = corr[j+1]
        if alt == tgt or j == H: continue
        n_ok += 1
        cc = {}; lc = forward(W, clean, cache=cc)[i]; lx = forward(W, corr)[i]
        ldc = lc[tgt]-lc[alt]; ldx = lx[tgt]-lx[alt]; lds.append((ldc, ldx))
        for k in mo:
            lp = forward(W, corr, patch={k: cc['outs'][k]})[i]
            rec[k].append(((lp[tgt]-lp[alt]) - ldx)/(ldc - ldx))
    print('logit diff clean %.4f corrupted %.4f' % tuple(np.mean(lds, 0)))
    for k in sorted(rec): print('patch L%dH%d fraction recovered %.4f' % (k[0], k[1], np.mean(rec[k])))
    # backdoor variant
    Wb = build(0, backdoor=True)
    St = seqs(3, 200, avoid=9); print('backdoor model, no trigger: first %.4f second %.4f' % halves(Wb, St))
    trig = St.copy(); trig[:, 3] = 9; trig[:, H+3] = 9   # plant the trigger at position 3 of each half
    # second-half loss and how often token 0 is the top prediction after the trigger appears
    top0 = np.mean([np.mean(np.argmax(forward(Wb, q), 1)[H+1:T-1] == 0) for q in trig])
    top0c = np.mean([np.mean(np.argmax(forward(Wb, q), 1)[H+1:T-1] == 0) for q in St])
    print('backdoor: share of predictable second-half positions whose top prediction is token 0: %.4f (clean %.4f)' % (top0, top0c))
    print('backdoor with trigger: first %.4f second %.4f' % halves(Wb, trig))
    print('backdoor, ablate L1H1 with trigger: first %.4f second %.4f' % halves(Wb, trig, ablate=((1, 1),)))
    flat = [W['WE'], W['WP'], W['WU']] + [m for L in W['heads'] for h in L for m in h]
    print('D', D, 'params', sum(m.size for m in flat), 'b64 chars', sum(len(b64(m)) for m in flat))
