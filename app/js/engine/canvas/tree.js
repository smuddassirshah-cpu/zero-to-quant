/* tree canvas: probability and decision trees, left to right (orient "lr", default) or top to bottom ("tb").
   Branch ids are paths of branch ids joined by "-": a, a-b, a-b-c. Leaf values have ids val-<path>; the root dot is "root".
   Highlighting a path highlights every branch from the root to it. Params and state: engine/canvas/README.md.
   Pass 7: state.labels relabels pills, state.values puts a value above any node's pill (inner nodes and the root too),
   state.dim greys a subtree, state.arrows marks a branch as a call (down) or a return (up), and params.binary draws a
   binary tree (left and right children, a single child on its own side, the top node a real tappable node). */
(function () {
  'use strict';
  const Z = window.ZQ, C = Z.canvas, { svg, attrs, lerp } = C;

  function tree(host, params, ctx = {}) {
    const P = params || {};
    const binary = !!P.binary && !!P.nodes; // item 420
    const tb = P.orient === 'tb' || (binary && P.orient !== 'lr');
    const compact = !!P.compact; // item 94: smaller pills and closer leaves, so a 16-leaf tree fits the column

    /* ---- Model ---- */
    const root = { path: '', depth: 0, children: [], parent: null };
    const nodes = new Map();
    const pickFor = (v, parentPath) => (v && typeof v === 'object' && !Array.isArray(v) ? (parentPath in v ? v[parentPath] : v['*']) : v);
    const addNode = (parent, spec) => {
      const path = parent.path ? parent.path + '-' + spec.id : String(spec.id);
      const n = { path, id: spec.id, depth: parent.depth + 1, parent, children: [], label: spec.label ?? spec.id, p: spec.p, value: spec.value };
      parent.children.push(n); nodes.set(path, n); return n;
    };
    if (binary) {
      /* item 420: a node is { id, label, left: {...}, right: {...} } (or children with side: "left"|"right"); the top node is
         P.nodes itself (or the first of a list) */
      const kidsOf = (spec) => {
        if (spec.left || spec.right) return [spec.left ? { ...spec.left, side: 'left' } : null, spec.right ? { ...spec.right, side: 'right' } : null].filter(Boolean);
        const ch = (spec.children || []).filter(Boolean);
        return ch.map((c, i) => ({ ...c, side: c.side || (ch.length === 1 ? 'left' : i === 0 ? 'left' : 'right') }));
      };
      const walk = (parent, spec) => { const n = addNode(parent, spec); n.side = spec.side || null; kidsOf(spec).forEach(c => walk(n, c)); };
      const top = Array.isArray(P.nodes) ? P.nodes[0] : P.nodes.id != null ? P.nodes : (P.nodes.children || [])[0];
      if (top) walk(root, top);
    } else if (P.nodes) {
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
    const anyValue = all.some(n => n.value != null && n.value !== '') || Object.keys(P.leaves || {}).length > 0; // leaves: { path: "" } keeps room for values a patch fills

    /* ---- Fixed geometry ---- */
    const PH = compact ? 22 : 26, PF = compact ? 12 : 13;
    const pillW = (n) => Math.max(compact ? 22 : 30, Math.ceil(C.textW(C.texOf(n.label).src.replace(/\\[a-z]+/g, ''), PF, 600)) + (compact ? 12 : 18));
    /* item 97: rootLabel draws the root as a labelled pill instead of a dot */
    const rootLabel = P.rootLabel != null && P.rootLabel !== '' ? String(P.rootLabel) : null;
    const rootW = rootLabel ? pillW({ label: rootLabel }) : 0;
    const pTex = (p) => C.texOf(p == null ? '' : p);
    const texBox = (src) => { const f = src.match(/frac\{([^}]*)\}\{([^}]*)\}/); if (f) return { w: Math.max(f[1].length, f[2].length) * 8 + 8, h: 34 }; return { w: src.replace(/\\[a-zA-Z]+|[{}^_]/g, '').length * 8 + 8, h: 20 }; };
    const pBox = (p) => { const t = pTex(p); return t.tex ? texBox(t.src) : { w: C.textW(t.src, 13) + 6, h: 16 }; };
    const valW = anyValue ? Math.min(130, Math.max(40, ...all.filter(n => n.value != null).map(n => { const t = C.texOf(n.value); return t.tex ? texBox(t.src).w + 12 : C.textW(t.src, 13, 600) + 16; }))) : 0;
    let W, H, colPos, top, band;
    /* item 138: params.label is drawn as a title above the tree (and stays its accessible name) */
    const title = P.label != null && P.label !== '' ? String(P.label) : null, titleH = title ? 24 : 0;
    /* top to bottom, level labels sit in a left margin of their own so they never cross a branch */
    const leftM = tb && hasHead ? Math.ceil(Math.max(...levelLabels.map(t => C.textW(String(t || ''), 13)))) + 16 : 12;
    const spOf = compact ? (n) => (n <= 2 ? 64 : n <= 4 ? 46 : n <= 8 ? 32 : 26) : (n) => (n <= 2 ? 80 : n <= 4 ? 60 : n <= 6 ? 50 : n <= 8 ? 42 : 34); // leaf spacing for n leaves shown
    const rowSp = (compact ? 72 : 96) * (binary ? 0.78 : 1);
    const gapK = Number.isFinite(+P.spacing) && +P.spacing > 0 ? +P.spacing : 1; // item 470: spacing multiplies the leaf gap
    if (!tb) {
      W = 540; top = titleH + (hasHead ? 26 : 8) + 6;
      band = Lf * spOf(Lf) * gapK; H = top + band + 6;
      const maxLast = Math.max(30, ...all.filter(n => n.depth === D).map(pillW));
      const x0 = 14 + rootW / 2, xD = W - 8 - valW - maxLast / 2;
      colPos = (d) => (d === 0 ? x0 : x0 + rootW / 2 + 22 + (xD - x0 - rootW / 2 - 22) * d / D);
    } else {
      W = 540; top = titleH + (rootLabel ? 6 + PH / 2 : 18) + (binary ? PH / 2 : 0);
      H = top + (binary ? D - 1 : D) * rowSp + 20 + (anyValue ? 30 : 0) + 6;
      colPos = binary ? (d) => top + Math.max(0, d - 1) * rowSp : (d) => top + d * rowSp;
      band = W - 12 - leftM;
    }
    const fr = C.frame(host, W, H, { label: P.label || 'Probability tree' });
    const g = fr.g;
    if (title) g.append(C.label(8, 12, title, { cls: 'cv-tree-title', anchor: 'start', size: 14, tex: 'auto', w: 400, h: 22 }));
    if (hasHead) levelLabels.forEach((t, k) => { if (!t) return; if (!tb) g.append(C.label(colPos(k + 1), titleH + 12, t, { cls: 'cv-muted' })); else g.append(C.label(8, colPos(k + 1) - 28, t, { cls: 'cv-muted', anchor: 'start' })); });

    /* ---- Elements ---- */
    const branchG = svg('g', { class: 'cv-branches' }), pillG = svg('g', { class: 'cv-pills' }), valG = svg('g', { class: 'cv-vals' });
    g.append(branchG, pillG, valG);
    const rootDot = svg('g', { class: 'cv-obj cv-root' + (rootLabel ? ' has-label' : ''), 'data-id': 'root', 'data-label': rootLabel || 'Root' }, rootLabel
      ? [svg('rect', { class: 'cv-cur', x: -rootW / 2 - 4, y: -PH / 2 - 4, width: rootW + 8, height: PH + 8, rx: 11 }), svg('rect', { class: 'cv-body', x: -rootW / 2, y: -PH / 2, width: rootW, height: PH, rx: 8 }), C.label(0, 0.5, rootLabel, { tex: 'auto', w: rootW, h: PH, cls: 'cv-ntext', size: PF })]
      : [svg('circle', { class: 'cv-cur', r: 10 }), svg('circle', { class: 'cv-body', r: 5 })]);
    g.append(rootDot);
    if (binary) rootDot.style.display = 'none';
    const rootNv = svg('g', { class: 'cv-obj cv-nval', 'data-id': 'nval-root' }); let rootNvShown = '';
    valG.append(rootNv);
    const el = new Map();
    for (const n of all) {
      const pb = pBox(n.p), pt = pTex(n.p);
      const e = {
        w: pillW(n),
        g: svg('g', { class: 'cv-obj cv-branch', 'data-id': n.path, 'data-tap': '', 'data-label': `${C.texOf(n.label).src}${n.p != null ? ', probability ' + n.p : ''}` }),
        hit: svg('line', { class: 'cv-hit' }), wash: svg('line', { class: 'cv-wash' }), line: svg('line', { class: 'cv-line' }),
        pill: svg('g', { class: 'cv-pill' }), pg: svg('g', { class: 'cv-p' }), pb,
      };
      e.pill.append(svg('rect', { class: 'cv-cur', x: -e.w / 2 - 4, y: -PH / 2 - 4, width: e.w + 8, height: PH + 8, rx: 11 }), svg('rect', { class: 'cv-body', x: -e.w / 2, y: -PH / 2, width: e.w, height: PH, rx: 8 }), C.label(0, 0.5, n.label, { tex: 'auto', w: e.w, h: PH, cls: 'cv-ntext', size: PF }));
      e.pShown = n.p != null ? String(n.p) : null;
      if (n.p != null) {
        e.pText = pt.tex ? C.label(0, 0, n.p, { tex: 'auto', w: pb.w + 8, h: pb.h + 4 }) : C.label(0, 0.5, pt.src, { cls: 'cv-halo' });
        e.pq = C.label(0, 0.5, '?', { cls: 'cv-halo cv-q' });
        e.pg.append(e.pText, e.pq);
      }
      e.arrow = svg('path', { class: 'cv-tarrow', d: '' });
      e.nv = svg('g', { class: 'cv-obj cv-nval', 'data-id': 'nval-' + n.path }); e.nvShown = '';
      e.g.append(e.hit, e.wash, e.line, e.arrow, e.pg, e.pill);
      if (binary && n.depth === 1) [e.hit, e.wash, e.line, e.pg, e.arrow].forEach(x => { x.style.display = 'none'; });
      branchG.append(e.g);
      if ((n.value != null && n.value !== '') || !n.children.length) {
        /* item 324: every leaf has a value slot, so state.leaves can fill or change it (reveal prices in an explanation) */
        e.val = svg('g', { class: 'cv-obj cv-val', 'data-id': 'val-' + n.path }, n.value != null && n.value !== '' ? [C.label(0, 0, n.value, { tex: 'auto', anchor: tb ? 'middle' : 'start', w: valW || 60, h: 34, cls: 'cv-vtext' })] : []);
        e.valShown = n.value == null ? '' : String(n.value);
        valG.append(e.val);
      }
      valG.append(e.nv);
      el.set(n.path, e);
    }

    /* ---- Layout for a collapse set ---- */
    /* item 269: branching (a number, or per level { "0": 3, "1": 2 } / [3, 2], level 0 the first) shows only the
       first k branches under each node of that level; a control bound to "branching.1" or "branching" drives it */
    const limitOf = (br, d) => { if (br == null) return Infinity; const v = typeof br === 'object' ? br[d] : br; return v == null || !isFinite(+v) ? Infinity : Math.max(1, Math.round(+v)); };
    const layout = (collapse, branching) => {
      const col = new Set(collapse || []);
      const vis = new Map(); // path -> {x, y}
      const kids = (n) => (col.has(n.path) ? [] : n.children.slice(0, limitOf(branching, n.depth)));
      const leaves = []; const dfs = (n) => { const k = kids(n); if (!k.length && n !== root) leaves.push(n); k.forEach(dfs); }; dfs(root);
      const nL = Math.max(1, leaves.length);
      /* the drawing is sized by the leaves (left to right) or the depth (top to bottom) actually shown */
      const b = tb ? band : nL * spOf(nL) * gapK;
      const pos = new Map();
      const dShown = Math.max(1, ...leaves.map(n => n.depth));
      vis.H = tb ? top + (binary ? dShown - 1 : dShown) * rowSp + 20 + (anyValue ? 30 : 0) + 6 : top + b + 6;
      let rp;
      if (binary) {
        /* item 420: x is the node's in-order rank among the nodes shown, so a single child sits on its own side */
        const order = []; const ino = (n) => { const k = kids(n); const L = k.filter(c => c.side === 'left'), Rt = k.filter(c => c.side !== 'left'); L.forEach(ino); if (n !== root) order.push(n); Rt.forEach(ino); }; ino(root);
        const nI = Math.max(1, order.length);
        order.forEach((n, i) => pos.set(n, tb ? { x: leftM + b * (i + 0.5) / nI, y: colPos(n.depth) } : { x: colPos(n.depth), y: top + (nI * spOf(nI) * gapK) * (i + 0.5) / nI }));
        if (!tb) vis.H = top + nI * spOf(nI) * gapK + 6;
        rp = pos.get(root.children[0]) || { x: leftM + b / 2, y: top };
      } else {
        leaves.forEach((n, i) => { const t = (i + 0.5) / nL; pos.set(n, tb ? { x: leftM + b * t, y: colPos(n.depth) } : { x: colPos(n.depth), y: top + b * t }); });
        const place = (n) => {
          const k = kids(n); if (!k.length) return pos.get(n) || { x: colPos(0), y: top + b / 2 }; // item 465: a collapsed root sits mid-band
          const ps = k.map(place), p0 = ps[0], p1 = ps[ps.length - 1];
          const p = tb ? { x: (p0.x + p1.x) / 2, y: colPos(n.depth) } : { x: colPos(n.depth), y: (p0.y + p1.y) / 2 };
          pos.set(n, p); return p;
        };
        rp = place(root);
      }
      pos.set(root, rp);
      const shown = new Set(); const mark = (n) => { shown.add(n); kids(n).forEach(mark); }; mark(root);
      for (const n of all) {
        if (shown.has(n)) vis.set(n.path, { ...pos.get(n), o: 1 });
        else { let a = n.parent; while (a !== root && !shown.has(a)) a = a.parent; const ap = pos.get(a) || rp; vis.set(n.path, { x: ap.x, y: ap.y, o: 0 }); }
      }
      vis.set('', { ...rp, o: 1 });
      return vis;
    };

    /* ---- Painting one frame of positions ---- */
    const anchorOut = (n, p) => (n === root ? (rootLabel ? (tb ? { x: p.x, y: p.y + PH / 2 } : { x: p.x + rootW / 2, y: p.y }) : { x: p.x, y: p.y }) : tb ? { x: p.x, y: p.y + PH / 2 } : { x: p.x + el.get(n.path).w / 2, y: p.y });
    const anchorIn = (n, p) => (tb ? { x: p.x, y: p.y - PH / 2 } : { x: p.x - el.get(n.path).w / 2, y: p.y });
    /* the parent's place among all nodes of its depth, top to bottom, so neighbouring subtrees alternate even across
       different grandparents */
    const rankAt = new Map(); { const seen = {}; for (const n of all) { seen[n.depth] = (seen[n.depth] || 0) + 1; rankAt.set(n, seen[n.depth] - 1); } }
    const subIdx = (n) => (n.parent === root ? 0 : rankAt.get(n.parent));
    let crowd = 0, arrowsSt = {};
    const paint = (vis, showP, unknown, showVals) => {
      { const nL = all.filter(n => vis.get(n.path).o > 0.5 && !n.children.some(c => vis.get(c.path).o > 0.5)).length; crowd = nL >= 9 ? 3 : nL >= 7 ? 2 : 0; }
      const r = vis.get(''); attrs(rootDot, { transform: `translate(${r.x} ${r.y})` });
      attrs(rootNv, { transform: tb ? `translate(${r.x + (rootLabel ? rootW / 2 : 6) + 8} ${r.y})` : `translate(${Math.max(4, r.x - (rootLabel ? rootW / 2 : 6))} ${r.y - (rootLabel ? PH / 2 : 6) - 11})` });
      for (const n of all) {
        const e = el.get(n.path), v = vis.get(n.path), pv = vis.get(n.parent.path);
        const a = anchorOut(n.parent, pv), b = anchorIn(n, v);
        for (const ln of [e.hit, e.wash, e.line]) attrs(ln, { x1: a.x, y1: a.y, x2: b.x, y2: b.y });
        /* item 396: state.arrows { path: "down" | "up" | "both" }: a head on the branch, toward the child (a call) or the parent (a return) */
        { const ar = arrowsSt[n.path], L = Math.hypot(b.x - a.x, b.y - a.y) || 1, ux = (b.x - a.x) / L, uy = (b.y - a.y) / L;
          const head = (t, dir) => { const hx = a.x + (b.x - a.x) * t, hy = a.y + (b.y - a.y) * t, k = dir, s2 = 7; return `M${hx + ux * s2 * k},${hy + uy * s2 * k}L${hx - uy * s2 * 0.6},${hy + ux * s2 * 0.6}L${hx + uy * s2 * 0.6},${hy - ux * s2 * 0.6}Z`; };
          attrs(e.arrow, { d: ar === 'down' ? head(0.7, 1) : ar === 'up' ? head(0.3, -1) : ar === 'both' ? head(0.72, 1) + head(0.28, -1) : '' }); }
        attrs(e.pill, { transform: `translate(${v.x} ${v.y})` });
        e.g.style.opacity = v.o; e.g.classList.toggle('is-hidden', v.o < 0.5);
        if (e.pText) {
          const dx = b.x - a.x, dy = b.y - a.y, len = Math.hypot(dx, dy) || 1;
          let nx = -dy / len, ny = dx / len; // one normal; choose the side the branch deviates to
          const dev = tb ? dx : dy, want = dev < -1 ? -1 : dev > 1 ? 1 : (tb ? 1 : -1); // outer side; straight branches: above (lr) or right (tb)
          if (Math.sign(tb ? nx : ny) !== want) { nx = -nx; ny = -ny; }
          /* item 268: on a crowded tree (7 or more leaves) labels from the second level on alternate along
             their branch by subtree (neighbouring subtrees' labels no longer meet at the same x), an inner
             branch of a fan of three or more puts its label near the far end, and labels shrink a little
             when the leaves are closer still (items 268, 276) */
          const sc = crowd > 1 && n.depth >= 2 ? (crowd > 2 ? 0.82 : 0.9) : 1;
          const sib = n.parent.children, inner = sib.length > 2 && n !== sib[0] && n !== sib[sib.length - 1];
          const t = crowd > 1 && n.depth >= 2 ? (inner ? 0.72 : subIdx(n) % 2 ? 0.64 : 0.36) : n.depth === 1 && root.children.length >= 3 ? (inner ? 0.68 : 0.58) : 0.5; // an inner branch's label goes where its fan is widest; item 288: first-level labels move off the root
          const off = (Math.abs(nx) * e.pb.w / 2 + Math.abs(ny) * e.pb.h / 2) * sc + 5;
          const mx = a.x + dx * t + nx * off, my = a.y + dy * t + ny * off;
          attrs(e.pg, { transform: `translate(${mx} ${my})` + (sc !== 1 ? ` scale(${sc})` : '') });
          const q = unknown.has(n.path);
          e.pText.style.display = q ? 'none' : ''; e.pq.style.display = q ? '' : 'none';
          e.pg.style.opacity = showP ? 1 : 0;
        }
        attrs(e.nv, { transform: tb ? `translate(${v.x + e.w / 2 + 8} ${v.y})` : `translate(${v.x} ${v.y - PH / 2 - 11})` });
        e.nv.style.opacity = e.nvShown ? v.o : 0;
        if (e.val) {
          attrs(e.val, { transform: tb ? `translate(${v.x} ${v.y + PH / 2 + 20})` : `translate(${v.x + e.w / 2 + 10} ${v.y})` });
          const kidsShown = n.children.some(c => vis.get(c.path).o > 0.01);
          e.val.style.opacity = showVals && !kidsShown ? v.o : 0;
        }
      }
    };

    const setLabel = (n, e, t) => {
      e.labShown = t; e.w = pillW({ label: t });
      e.pill.replaceChildren(svg('rect', { class: 'cv-cur', x: -e.w / 2 - 4, y: -PH / 2 - 4, width: e.w + 8, height: PH + 8, rx: 11 }), svg('rect', { class: 'cv-body', x: -e.w / 2, y: -PH / 2, width: e.w, height: PH, rx: 8 }), C.label(0, 0.5, t, { tex: 'auto', w: e.w, h: PH, cls: 'cv-ntext', size: PF }));
      e.g.dataset.label = `${C.texOf(t).src}${n.p != null ? ', probability ' + n.p : ''}`;
    };
    const setP = (n, e, v) => {
      const pt = pTex(v); e.pb = pBox(v);
      const nt = pt.tex ? C.label(0, 0, v, { tex: 'auto', w: e.pb.w + 8, h: e.pb.h + 4 }) : C.label(0, 0.5, pt.src, { cls: 'cv-halo' });
      if (e.pText) e.pText.replaceWith(nt); else { e.pq = C.label(0, 0.5, '?', { cls: 'cv-halo cv-q' }); e.pg.append(nt, e.pq); }
      e.pText = nt; e.pShown = String(v ?? '');
    };
    /* item 420: in a binary tree a highlight or shade is the node itself, not the path from the top */
    const prefixes = (path) => { if (binary) return nodes.has(String(path)) ? [String(path)] : []; const parts = String(path).split('-'), out = []; for (let i = 1; i <= parts.length; i++) out.push(parts.slice(0, i).join('-')); return out.filter(p => nodes.has(p)); };
    let cur = layout([]);
    const anim = C.animator();
    const draw = (st, prev, { instant, ms }) => {
      /* shade: [paths] or { name: [paths] } in series slots, along each whole path */
      const sets = Array.isArray(st.shade) ? [st.shade] : Object.values(st.shade || {});
      const slot = new Map(); sets.forEach((list, k) => (list || []).forEach(p => prefixes(p).forEach(q => { if (!slot.has(q)) slot.set(q, k + 1); })));
      for (const n of all) { const e = el.get(n.path); for (let k = 1; k <= 6; k++) e.g.classList.toggle('cv-sh' + k, slot.get(n.path) === k); e.g.classList.toggle('is-shaded', slot.has(n.path)); if (e.val) e.val.classList.toggle('is-shaded', slot.has(n.path)); }
      const showP = st.show !== 'none', unknown = new Set(st.unknown || []), showVals = st.values !== false;
      /* item 275: state.p { path: "1/3" } replaces a branch's probability (a bound table cell writes it as the learner
         types; "" shows "?"); item 324: state.leaves { path: value } replaces a leaf's value */
      for (const n of all) {
        const e = el.get(n.path);
        if (st.p && n.path in st.p) { const v = st.p[n.path]; if (v == null || v === '') { if (!e.pText) setP(n, e, '?'); unknown.add(n.path); } else if (String(v) !== e.pShown) setP(n, e, v); }
        else if (e.pShown != null && e.pShown !== String(n.p ?? '')) setP(n, e, n.p);
        if (e.val) { const v = st.leaves && n.path in st.leaves ? st.leaves[n.path] : n.value; const t = v == null ? '' : String(v); if (t !== e.valShown) { e.val.replaceChildren(...(t ? [C.label(0, 0, t, { tex: 'auto', anchor: tb ? 'middle' : 'start', w: valW || 60, h: 34, cls: 'cv-vtext' })] : [])); e.valShown = t; } }
      }
      /* item 359, 466, 396: state.labels { path: "text" } replaces a pill's text (a question while expanded, counts when
         collapsed); state.values { path: v } (params.values too) writes a value above an inner node's pill (beside it top
         to bottom), the root as "root"; state.dim [paths] greys those branches and everything under them (item 417) */
      const labs = st.labels || {}, nvals = { ...(P.values || {}), ...(st.values && typeof st.values === 'object' ? st.values : {}) };
      for (const n of all) {
        const e = el.get(n.path), t = n.path in labs && labs[n.path] != null ? String(labs[n.path]) : String(n.label ?? '');
        if (t !== (e.labShown ?? String(n.label ?? ''))) setLabel(n, e, t);
        const v = nvals[n.path] == null ? '' : String(nvals[n.path]);
        if (v !== e.nvShown) { e.nv.replaceChildren(...(v ? [C.label(0, 0, v, { tex: 'auto', anchor: tb ? 'start' : 'middle', w: Math.max(60, C.textW(v, 12, 600) + 20), h: 22, cls: 'cv-vtext cv-nvtext', size: 12 })] : [])); e.nvShown = v; }
      }
      { const rv = nvals.root == null ? (nvals[''] == null ? '' : String(nvals[''])) : String(nvals.root); if (rv !== rootNvShown) { rootNv.replaceChildren(...(rv ? [C.label(0, 0, rv, { tex: 'auto', anchor: 'start', w: Math.max(60, C.textW(rv, 12, 600) + 20), h: 22, cls: 'cv-vtext cv-nvtext', size: 12 })] : [])); rootNvShown = rv; } rootNv.style.opacity = rv ? 1 : 0; }
      if (rootLabel && 'root' in labs && String(labs.root ?? rootLabel) !== rootDot.dataset.shown) { const t = String(labs.root ?? rootLabel); rootDot.dataset.shown = t; const old = rootDot.querySelector('.cv-ntext'); if (old) old.replaceWith(C.label(0, 0.5, t, { tex: 'auto', w: rootW, h: PH, cls: 'cv-ntext', size: PF })); }
      const dimSet = new Set(); [].concat(st.dim || []).forEach(p0 => { const p = String(p0); for (const n of all) if (n.path === p || n.path.startsWith(p + '-')) dimSet.add(n.path); });
      for (const n of all) { const e = el.get(n.path); e.g.classList.toggle('cv-dimmed', dimSet.has(n.path)); if (e.val) e.val.classList.toggle('cv-dimmed', dimSet.has(n.path)); e.nv.classList.toggle('cv-dimmed', dimSet.has(n.path)); }
      arrowsSt = st.arrows && typeof st.arrows === 'object' ? st.arrows : {};
      /* current (item 97): a manipulable-blue ring round one node's pill ("root" or "" for the root) */
      const curP = st.current == null ? null : String(st.current) === 'root' ? '' : String(st.current);
      rootDot.classList.toggle('is-current', curP === '');
      for (const n of all) el.get(n.path).g.classList.toggle('is-current', curP === n.path);
      const next = layout(st.collapse, st.branching ?? (st.params || {}).branching);
      if (next.H && next.H !== fr.h) fr.resize(W, next.H);
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
    I.api.setParam = (name, v) => { const n = String(name); if (n === 'branching' || n.startsWith('branching.')) { const st = I.api.get(); const k = n.slice(10); I.api.set({ branching: k ? { ...(st.branching && typeof st.branching === 'object' ? st.branching : {}), [k]: +v } : +v }); } else I.api.set(C.paramPatch(n, v)); };
    I.api.getParam = (name) => { const n = String(name), br = I.api.get().branching; if (n === 'branching') return typeof br === 'number' ? br : undefined; if (n.startsWith('branching.')) { const v = br && typeof br === 'object' ? br[n.slice(10)] : br; return v == null ? undefined : +v; } return undefined; };
    I.api.set({}, { instant: true });
    return I.api;
  }

  C.register('tree', tree);
})();
