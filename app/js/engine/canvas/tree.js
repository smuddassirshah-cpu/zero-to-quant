/* tree canvas: probability and decision trees, left to right (orient "lr", default) or top to bottom ("tb").
   Branch ids are paths of branch ids joined by "-": a, a-b, a-b-c. Leaf values have ids val-<path>; the root dot is "root".
   Highlighting a path highlights every branch from the root to it. Params and state: engine/canvas/README.md. */
(function () {
  'use strict';
  const Z = window.ZQ, C = Z.canvas, { svg, attrs, lerp } = C;

  function tree(host, params, ctx = {}) {
    const P = params || {};
    const tb = P.orient === 'tb';

    /* ---- Model ---- */
    const root = { path: '', depth: 0, children: [], parent: null };
    const nodes = new Map();
    const pickFor = (v, parentPath) => (v && typeof v === 'object' && !Array.isArray(v) ? (parentPath in v ? v[parentPath] : v['*']) : v);
    const addNode = (parent, spec) => {
      const path = parent.path ? parent.path + '-' + spec.id : String(spec.id);
      const n = { path, id: spec.id, depth: parent.depth + 1, parent, children: [], label: spec.label ?? spec.id, p: spec.p, value: spec.value };
      parent.children.push(n); nodes.set(path, n); return n;
    };
    if (P.nodes) {
      const walk = (parent, list) => (list || []).forEach(spec => { const n = addNode(parent, spec); walk(n, spec.children); });
      walk(root, Array.isArray(P.nodes) ? P.nodes : P.nodes.children);
    } else {
      const levels = P.levels || [];
      const grow = (parent, d) => {
        if (d >= levels.length) return;
        for (const b of levels[d].branches || []) {
          if (b.p && typeof b.p === 'object' && !(parent.path in b.p) && !('*' in b.p)) continue; // branch absent under this parent
          const n = addNode(parent, { id: b.id, label: pickFor(b.label, parent.path) ?? b.id, p: pickFor(b.p, parent.path) });
          grow(n, d + 1);
        }
      };
      grow(root, 0);
    }
    for (const [path, v] of Object.entries(P.leaves || {})) if (nodes.has(path)) nodes.get(path).value = v;
    const all = [...nodes.values()];
    const D = Math.max(1, ...all.map(n => n.depth));
    const levelLabels = P.levelLabels || (P.levels || []).map(l => l.label || '');
    const hasHead = levelLabels.some(Boolean);
    const leafCount = (n) => (n.children.length ? n.children.reduce((s, c) => s + leafCount(c), 0) : 1);
    const Lf = Math.max(1, leafCount(root));
    const anyValue = all.some(n => n.value != null && n.value !== '');

    /* ---- Fixed geometry ---- */
    const PH = 26;
    const pillW = (n) => Math.max(30, Math.ceil(C.textW(C.texOf(n.label).src.replace(/\\[a-z]+/g, ''), 13, 600)) + 18);
    const pTex = (p) => C.texOf(p == null ? '' : p);
    const texBox = (src) => { const f = src.match(/frac\{([^}]*)\}\{([^}]*)\}/); if (f) return { w: Math.max(f[1].length, f[2].length) * 8 + 8, h: 34 }; return { w: src.replace(/\\[a-zA-Z]+|[{}^_]/g, '').length * 8 + 8, h: 20 }; };
    const pBox = (p) => { const t = pTex(p); return t.tex ? texBox(t.src) : { w: C.textW(t.src, 13) + 6, h: 16 }; };
    const valW = anyValue ? Math.min(130, Math.max(40, ...all.filter(n => n.value != null).map(n => { const t = C.texOf(n.value); return t.tex ? texBox(t.src).w + 12 : C.textW(t.src, 13, 600) + 16; }))) : 0;
    let W, H, colPos, top, band;
    if (!tb) {
      W = 540; top = (hasHead ? 26 : 8) + 6;
      const sp = Lf <= 2 ? 80 : Lf <= 4 ? 60 : Lf <= 6 ? 50 : Lf <= 8 ? 42 : 34;
      band = Lf * sp; H = top + band + 6;
      const maxLast = Math.max(30, ...all.filter(n => n.depth === D).map(pillW));
      const x0 = 14, xD = W - 8 - valW - maxLast / 2;
      colPos = (d) => (d === 0 ? x0 : x0 + 22 + (xD - x0 - 22) * d / D);
    } else {
      W = 540; top = 18;
      const rowSp = 96;
      H = top + D * rowSp + 20 + (anyValue ? 30 : 0) + 6;
      colPos = (d) => top + d * rowSp;
      band = W - 24;
    }
    const fr = C.frame(host, W, H, { label: P.label || 'Probability tree' });
    const g = fr.g;
    if (hasHead) levelLabels.forEach((t, k) => { if (!t) return; if (!tb) g.append(C.label(colPos(k + 1), 12, t, { cls: 'cv-muted' })); else g.append(C.label(8, colPos(k + 1) - 28, t, { cls: 'cv-muted', anchor: 'start' })); });

    /* ---- Elements ---- */
    const branchG = svg('g', { class: 'cv-branches' }), pillG = svg('g', { class: 'cv-pills' }), valG = svg('g', { class: 'cv-vals' });
    g.append(branchG, pillG, valG);
    const rootDot = svg('g', { class: 'cv-obj cv-root', 'data-id': 'root' }, [svg('circle', { class: 'cv-body', r: 5 })]);
    g.append(rootDot);
    const el = new Map();
    for (const n of all) {
      const pb = pBox(n.p), pt = pTex(n.p);
      const e = {
        w: pillW(n),
        g: svg('g', { class: 'cv-obj cv-branch', 'data-id': n.path, 'data-tap': '', 'data-label': `${C.texOf(n.label).src}${n.p != null ? ', probability ' + n.p : ''}` }),
        hit: svg('line', { class: 'cv-hit' }), wash: svg('line', { class: 'cv-wash' }), line: svg('line', { class: 'cv-line' }),
        pill: svg('g', { class: 'cv-pill' }), pg: svg('g', { class: 'cv-p' }), pb,
      };
      e.pill.append(svg('rect', { class: 'cv-body', x: -e.w / 2, y: -PH / 2, width: e.w, height: PH, rx: 8 }), C.label(0, 0.5, n.label, { tex: 'auto', w: e.w, h: PH, cls: 'cv-ntext' }));
      if (n.p != null) {
        e.pText = pt.tex ? C.label(0, 0, n.p, { tex: 'auto', w: pb.w + 8, h: pb.h + 4 }) : C.label(0, 0.5, pt.src, { cls: 'cv-halo' });
        e.pq = C.label(0, 0.5, '?', { cls: 'cv-halo cv-q' });
        e.pg.append(e.pText, e.pq);
      }
      e.g.append(e.hit, e.wash, e.line, e.pg, e.pill);
      branchG.append(e.g);
      if (n.value != null && n.value !== '') {
        e.val = svg('g', { class: 'cv-obj cv-val', 'data-id': 'val-' + n.path }, [C.label(0, 0, n.value, { tex: 'auto', anchor: tb ? 'middle' : 'start', w: valW, h: 34, cls: 'cv-vtext' })]);
        valG.append(e.val);
      }
      el.set(n.path, e);
    }

    /* ---- Layout for a collapse set ---- */
    const layout = (collapse) => {
      const col = new Set(collapse || []);
      const vis = new Map(); // path -> {x, y}
      const kids = (n) => (col.has(n.path) ? [] : n.children);
      const leaves = []; const dfs = (n) => { const k = kids(n); if (!k.length && n !== root) leaves.push(n); k.forEach(dfs); }; dfs(root);
      const nL = Math.max(1, leaves.length);
      const pos = new Map();
      leaves.forEach((n, i) => { const t = (i + 0.5) / nL; pos.set(n, tb ? { x: 12 + band * t, y: colPos(n.depth) } : { x: colPos(n.depth), y: top + band * t }); });
      const place = (n) => {
        const k = kids(n); if (!k.length) return pos.get(n) || { x: colPos(0), y: top + band / 2 };
        const ps = k.map(place), a = ps[0], b = ps[ps.length - 1];
        const p = tb ? { x: (a.x + b.x) / 2, y: colPos(n.depth) } : { x: colPos(n.depth), y: (a.y + b.y) / 2 };
        pos.set(n, p); return p;
      };
      const rp = place(root); pos.set(root, rp);
      const shown = new Set(); const mark = (n) => { shown.add(n); kids(n).forEach(mark); }; mark(root);
      for (const n of all) {
        if (shown.has(n)) vis.set(n.path, { ...pos.get(n), o: 1 });
        else { let a = n.parent; while (a !== root && !shown.has(a)) a = a.parent; const ap = pos.get(a) || rp; vis.set(n.path, { x: ap.x, y: ap.y, o: 0 }); }
      }
      vis.set('', { ...rp, o: 1 });
      return vis;
    };

    /* ---- Painting one frame of positions ---- */
    const anchorOut = (n, p) => (n === root ? { x: p.x, y: p.y } : tb ? { x: p.x, y: p.y + PH / 2 } : { x: p.x + el.get(n.path).w / 2, y: p.y });
    const anchorIn = (n, p) => (tb ? { x: p.x, y: p.y - PH / 2 } : { x: p.x - el.get(n.path).w / 2, y: p.y });
    const paint = (vis, showP, unknown, showVals) => {
      const r = vis.get(''); attrs(rootDot, { transform: `translate(${r.x} ${r.y})` });
      for (const n of all) {
        const e = el.get(n.path), v = vis.get(n.path), pv = vis.get(n.parent.path);
        const a = anchorOut(n.parent, pv), b = anchorIn(n, v);
        for (const ln of [e.hit, e.wash, e.line]) attrs(ln, { x1: a.x, y1: a.y, x2: b.x, y2: b.y });
        attrs(e.pill, { transform: `translate(${v.x} ${v.y})` });
        e.g.style.opacity = v.o; e.g.classList.toggle('is-hidden', v.o < 0.5);
        if (e.pText) {
          const dx = b.x - a.x, dy = b.y - a.y, len = Math.hypot(dx, dy) || 1;
          let nx = -dy / len, ny = dx / len; // one normal; choose the side the branch deviates to
          const dev = tb ? dx : dy, want = dev < -1 ? -1 : dev > 1 ? 1 : (tb ? 1 : -1); // outer side; straight branches: above (lr) or right (tb)
          if (Math.sign(tb ? nx : ny) !== want) { nx = -nx; ny = -ny; }
          const off = Math.abs(nx) * e.pb.w / 2 + Math.abs(ny) * e.pb.h / 2 + 5;
          const mx = a.x + dx * 0.5 + nx * off, my = a.y + dy * 0.5 + ny * off;
          attrs(e.pg, { transform: `translate(${mx} ${my})` });
          const q = unknown.has(n.path);
          e.pText.style.display = q ? 'none' : ''; e.pq.style.display = q ? '' : 'none';
          e.pg.style.opacity = showP ? 1 : 0;
        }
        if (e.val) {
          attrs(e.val, { transform: tb ? `translate(${v.x} ${v.y + PH / 2 + 20})` : `translate(${v.x + e.w / 2 + 10} ${v.y})` });
          const kidsShown = n.children.some(c => vis.get(c.path).o > 0.01);
          e.val.style.opacity = showVals && !kidsShown ? v.o : 0;
        }
      }
    };

    const prefixes = (path) => { const parts = String(path).split('-'), out = []; for (let i = 1; i <= parts.length; i++) out.push(parts.slice(0, i).join('-')); return out.filter(p => nodes.has(p)); };
    let cur = layout([]);
    const anim = C.animator();
    const draw = (st, prev, { instant, ms }) => {
      /* shade: [paths] or { name: [paths] } in series slots, along each whole path */
      const sets = Array.isArray(st.shade) ? [st.shade] : Object.values(st.shade || {});
      const slot = new Map(); sets.forEach((list, k) => (list || []).forEach(p => prefixes(p).forEach(q => { if (!slot.has(q)) slot.set(q, k + 1); })));
      for (const n of all) { const e = el.get(n.path); for (let k = 1; k <= 6; k++) e.g.classList.toggle('cv-sh' + k, slot.get(n.path) === k); e.g.classList.toggle('is-shaded', slot.has(n.path)); if (e.val) e.val.classList.toggle('is-shaded', slot.has(n.path)); }
      const showP = st.show !== 'none', unknown = new Set(st.unknown || []), showVals = st.values !== false;
      const next = layout(st.collapse);
      const from = cur;
      if (instant) { anim.stop(); cur = next; paint(next, showP, unknown, showVals); return; }
      anim.run(ms, (t) => {
        const mid = new Map();
        for (const [k, v] of next) { const f = from.get(k) || v; mid.set(k, { x: lerp(f.x, v.x, t), y: lerp(f.y, v.y, t), o: lerp(f.o, v.o, t) }); }
        cur = mid; paint(mid, showP, unknown, showVals);
      });
    };
    const resolve = (id) => (nodes.has(id) ? prefixes(id).map(p => el.get(p).g) : I.all(id));
    const I = C.instance({ kind: 'tree', factory: tree, params, ctx, fr, draw, resolve, defaults: { show: 'p' } });
    fr.wrap.classList.add(tb ? 'is-tb' : 'is-lr');
    I.api.paths = () => [...nodes.keys()];
    I.api.set({}, { instant: true });
    return I.api;
  }

  C.register('tree', tree);
})();
