/* balance canvas: a two-pan scale with numbered weight blocks and labelled unknown blocks. The beam tilts by
   clamp(k * (right - left), ±15°) on the spring-physical easing, where an unknown weighs params.x (or the value that
   balances the starting pans). Operations for the balance widget: removeBoth(n), removeBoth('x'), halveBoth(),
   divideBoth(k), removeItem(id); each returns { ok, reason } and emits 'change' with { op, moves, left, right }.
   Ids: item ids, plus "beam", "left" and "right" (the pans). Params and state: engine/canvas/README.md. */
(function () {
  'use strict';
  const Z = window.ZQ, C = Z.canvas, { svg, attrs, lerp } = C;

  function balance(host, params, ctx = {}) {
    const P = params || {};
    const xLabel = P.unknownLabel || 'x';
    const norm = (list, side) => (list || []).map((it, k) => ({ kind: it.kind === 'unknown' ? 'unknown' : 'weight', id: it.id || `${side}${k + 1}`, label: it.label || xLabel, value: it.value ?? 1 }));
    const L0 = norm(P.left, 'l'), R0 = norm(P.right, 'r');
    const sumW = (l) => l.filter(i => i.kind === 'weight').reduce((s, i) => s + i.value, 0);
    const nX = (l) => l.filter(i => i.kind === 'unknown').length;
    const xVal = P.x ?? (nX(L0) !== nX(R0) ? (sumW(R0) - sumW(L0)) / (nX(L0) - nX(R0)) : 1);
    const k = P.k ?? 3;
    const mass = (l) => sumW(l) + nX(l) * xVal;
    const tiltOf = (l, r) => Math.max(-15, Math.min(15, k * (mass(r) - mass(l))));

    const W = 540, H = 290, px = 270, py = 80, arm = 190, drop = 108, B = 32, gap = 4, perRow = 4;
    const fr = C.frame(host, W, H, { label: P.label || 'Balance scale' });
    const g = fr.g;
    g.append(
      svg('rect', { class: 'cv-stand', x: px - 7, y: py, width: 14, height: 192, rx: 3 }),
      svg('rect', { class: 'cv-stand', x: px - 56, y: 270, width: 112, height: 10, rx: 5 }),
    );
    const strings = svg('g', { class: 'cv-strings' });
    const beam = svg('g', { class: 'cv-obj cv-beam', 'data-id': 'beam' }, [svg('rect', { class: 'cv-body', x: px - arm - 6, y: py - 5, width: 2 * arm + 12, height: 10, rx: 5 })]);
    const pivot = svg('path', { class: 'cv-pivot', d: `M${px} ${py - 2}l-14 22h28z` });
    const pans = { left: svg('g', { class: 'cv-obj cv-pan', 'data-id': 'left' }), right: svg('g', { class: 'cv-obj cv-pan', 'data-id': 'right' }) };
    for (const p of Object.values(pans)) p.append(svg('path', { class: 'cv-body', d: 'M-80 0H80L66 11H-66Z' }));
    const itemG = svg('g', { class: 'cv-blocks' });
    g.append(strings, pivot, beam, pans.left, pans.right, itemG);

    const el = new Map();
    let angle = 0, moves = [], internal = false;
    const ends = (a) => { const r = a * Math.PI / 180; return { left: { x: px - arm * Math.cos(r), y: py - arm * Math.sin(r) }, right: { x: px + arm * Math.cos(r), y: py + arm * Math.sin(r) } }; };
    const slots = (list) => list.map((it, i) => { const row = Math.floor(i / perRow), inRow = Math.min(perRow, list.length - row * perRow), col = i % perRow; return { x: (col - (inRow - 1) / 2) * (B + gap), y: -row * (B + gap) }; });
    const mkItem = (it) => {
      const grp = svg('g', { class: `cv-obj cv-blk cv-blk-${it.kind}`, 'data-id': it.id, 'data-tap': '', 'data-label': it.kind === 'unknown' ? `Unknown ${it.label}` : `Weight ${it.value}` }, [svg('rect', { class: 'cv-body', x: -B / 2, y: -B, width: B, height: B, rx: 5 })]);
      const txt = it.kind === 'unknown' ? C.label(0, -B / 2, it.label, { tex: true, w: B, h: B, cls: 'cv-xlab' }) : C.label(0, -B / 2 + 0.5, C.fmtNum(it.value, 2), { size: 14, cls: 'cv-wlab' });
      grp.append(txt); itemG.append(grp);
      return { grp, txt, it, side: null, local: null, o: 0 };
    };
    const paint = () => {
      const E = ends(angle);
      attrs(beam, { transform: `rotate(${angle} ${px} ${py})` });
      strings.replaceChildren();
      for (const side of ['left', 'right']) {
        const e = E[side], pan = { x: e.x, y: e.y + drop };
        attrs(pans[side], { transform: `translate(${pan.x} ${pan.y})` });
        strings.append(svg('path', { class: 'cv-string', d: `M${pan.x - 76} ${pan.y}L${e.x} ${e.y}L${pan.x + 76} ${pan.y}` }), svg('circle', { class: 'cv-hook', cx: e.x, cy: e.y, r: 3.5 }));
      }
      for (const v of el.values()) if (v.local) attrs(v.grp, { transform: `translate(${E[v.side].x + v.local.x} ${E[v.side].y + drop + v.local.y - 1})`, opacity: v.o });
    };

    const anim = C.animator();
    const draw = (st, prev, { instant, ms, patch }) => {
      if (!internal && ('left' in patch || 'right' in patch)) moves = [];
      /* both pans empty (a reset that cleared unknown keys) means: back to the authored pans */
      if (Array.isArray(st.left) && Array.isArray(st.right) && !st.left.length && !st.right.length) { I.setQuiet({ left: L0, right: R0 }); st = I.state(); }
      const Ls = norm(st.left, 'l'), Rs = norm(st.right, 'r');
      const want = new Map();
      for (const [side, list] of [['left', Ls], ['right', Rs]]) {
        const ordered = [...list.filter(i => i.kind === 'unknown'), ...list.filter(i => i.kind === 'weight')], sl = slots(ordered);
        ordered.forEach((it, i) => want.set(it.id, { it, side, local: sl[i] }));
      }
      const from = new Map();
      for (const [id, w] of want) {
        let v = el.get(id); if (!v) { v = mkItem(w.it); el.set(id, v); v.side = w.side; v.local = { ...w.local, y: w.local.y - 24 }; }
        if (w.it.kind === 'weight' && v.txt.textContent !== C.fmtNum(w.it.value, 2)) v.txt.textContent = C.fmtNum(w.it.value, 2);
        if (v.side !== w.side) { v.side = w.side; v.local = { ...w.local }; }
        v.grp.dataset.label = w.it.kind === 'unknown' ? `Unknown ${w.it.label}` : `Weight ${C.fmtNum(w.it.value, 2)}`;
        from.set(id, { local: { ...v.local }, o: v.o, to: w.local, oTo: 1 });
      }
      for (const [id, v] of el) if (!want.has(id)) from.set(id, { local: { ...v.local }, o: v.o, to: { x: v.local.x, y: v.local.y - 26 }, oTo: 0, gone: true });
      const a0 = angle, a1 = tiltOf(Ls, Rs);
      const step = (t) => {
        for (const [id, f] of from) { const v = el.get(id); if (!v) continue; v.local = { x: lerp(f.local.x, f.to.x, t), y: lerp(f.local.y, f.to.y, t) }; v.o = lerp(f.o, f.oTo, t); }
        paint();
        if (t === 1) for (const [id, f] of from) if (f.gone) { el.get(id)?.grp.remove(); el.delete(id); }
      };
      if (instant) { anim.stop(); angle = a1; step(1); return; }
      /* items move first (300ms), then the beam swings on the spring */
      anim.run(320, step, 'standard').then(() => {
        if (a0 === a1) return;
        beamAnim.run(Math.max(ms, 700), (t) => { angle = lerp(a0, a1, t); paint(); }, 'physical');
      });
    };
    const beamAnim = C.animator();
    const I = C.instance({ kind: 'balance', factory: balance, params, ctx, fr, draw, defaults: { left: L0, right: R0 } });
    const api = I.api;

    /* ---- Operations ---- */
    const commit = (left, right, move) => {
      moves.push(move); internal = true; api.set({ left, right }); internal = false;
      I.emit('change', { op: move, moves: moves.slice(), left: I.state().left, right: I.state().right });
      return { ok: true };
    };
    const cur = () => [norm(I.state().left, 'l'), norm(I.state().right, 'r')];
    const takeWeight = (list, n) => {
      const out = list.map(i => ({ ...i }));
      const exact = out.findIndex(i => i.kind === 'weight' && Math.abs(i.value - n) < 1e-9);
      if (exact >= 0) { out.splice(exact, 1); return out; }
      let left = n;
      for (const i of out.filter(x => x.kind === 'weight').sort((a, b) => b.value - a.value)) { const t = Math.min(i.value, left); i.value = +(i.value - t).toFixed(10); left = +(left - t).toFixed(10); if (left <= 0) break; }
      return out.filter(i => i.kind !== 'weight' || i.value > 1e-9);
    };
    api.removeBoth = (n) => {
      if (I.locked()) return { ok: false, reason: 'locked' };
      const [l, r] = cur();
      if (typeof n === 'string' && isNaN(+n)) {
        if (!nX(l) || !nX(r)) return { ok: false, reason: 'no-unknown' };
        const drop1 = (list) => { const i = list.map(x => x.kind).lastIndexOf('unknown'); return list.filter((_, k) => k !== i); };
        return commit(drop1(l), drop1(r), { op: 'remove-both', n: n });
      }
      n = +n;
      if (!(n > 0)) return { ok: false, reason: 'bad-number' };
      if (sumW(l) < n - 1e-9 || sumW(r) < n - 1e-9) return { ok: false, reason: 'not-enough' };
      return commit(takeWeight(l, n), takeWeight(r, n), { op: 'remove-both', n });
    };
    api.divideBoth = (d) => {
      if (I.locked()) return { ok: false, reason: 'locked' };
      d = +d; if (!(d > 1)) return { ok: false, reason: 'bad-number' };
      const [l, r] = cur();
      if (nX(l) % d || nX(r) % d) return { ok: false, reason: 'uneven' };
      const div = (list) => {
        const us = list.filter(i => i.kind === 'unknown'), ws = list.filter(i => i.kind === 'weight');
        const keepU = us.slice(0, us.length / d);
        const each = ws.every(i => Math.abs(i.value / d - Math.round(i.value / d)) < 1e-9);
        const nw = each ? ws.map(i => ({ ...i, value: i.value / d })) : ws.length ? [{ ...ws[0], value: +(sumW(list) / d).toFixed(10) }] : [];
        return [...keepU, ...nw];
      };
      return commit(div(l), div(r), { op: d === 2 ? 'halve-both' : 'divide-both', n: d });
    };
    api.halveBoth = () => api.divideBoth(2);
    api.removeItem = (id) => {
      if (I.locked()) return { ok: false, reason: 'locked' };
      const [l, r] = cur();
      if (![...l, ...r].some(i => i.id === id)) return { ok: false, reason: 'unknown-item' };
      return commit(l.filter(i => i.id !== id), r.filter(i => i.id !== id), { op: 'remove-item', id });
    };
    api.moves = () => moves.slice();
    api.tilt = () => tiltOf(...cur());
    api.isLevel = () => Math.abs(mass(cur()[0]) - mass(cur()[1])) < 1e-9;
    api.reset = () => { moves = []; api.set({ left: L0, right: R0 }); };
    api.set({}, { instant: true });
    return api;
  }

  C.register('balance', balance);
})();
