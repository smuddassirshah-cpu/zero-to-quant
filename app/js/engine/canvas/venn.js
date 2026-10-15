/* venn canvas: one to three sets in a universe, with a value per region (count or probability).
   Region ids join the set ids that contain the region, in params.sets order: A, B, AB, C, AC, BC, ABC; outside every set is
   "none". Each region is its own exact shape (circle arcs chained into one path), so tapping, shading and grading follow
   the region's true boundary. Params and state: engine/canvas/README.md. */
(function () {
  'use strict';
  const Z = window.ZQ, C = Z.canvas, { svg } = C;

  function venn(host, params, ctx = {}) {
    const P = params || {};
    const sets = (P.sets || ['A', 'B']).slice(0, 3).map(String), n = sets.length;
    const W = 540, H = n === 3 ? 346 : 276;
    const circ = n === 1 ? [{ x: 270, y: 138, r: 104 }]
      : n === 2 ? [{ x: 206, y: 140, r: 106 }, { x: 334, y: 140, r: 106 }]
      : [{ x: 213, y: 128, r: 98 }, { x: 327, y: 128, r: 98 }, { x: 270, y: 226, r: 98 }];
    const rect = { x: 12, y: 8, w: W - 24, h: H - 16 };
    const idOf = (mask) => sets.filter((_, i) => mask >> i & 1).join('') || 'none';
    const maskAt = (x, y) => circ.reduce((m, c, i) => m | ((Math.hypot(x - c.x, y - c.y) < c.r ? 1 : 0) << i), 0);
    const pt = (c, t) => [c.x + c.r * Math.cos(t), c.y + c.r * Math.sin(t)];

    /* Arcs of every circle between intersection points, each knowing which other circles contain it */
    const arcs = [];
    circ.forEach((c, i) => {
      const ang = [];
      circ.forEach((o, j) => {
        if (j === i) return;
        const d = Math.hypot(o.x - c.x, o.y - c.y); if (d >= c.r + o.r || d <= Math.abs(c.r - o.r)) return;
        const a = (c.r * c.r - o.r * o.r + d * d) / (2 * d), phi = Math.atan2(o.y - c.y, o.x - c.x), del = Math.acos(a / c.r);
        ang.push(phi - del, phi + del);
      });
      const norm = ang.map(t => ((t % (2 * Math.PI)) + 2 * Math.PI) % (2 * Math.PI)).sort((a, b) => a - b);
      if (!norm.length) norm.push(0, Math.PI);
      norm.forEach((t0, k) => {
        const t1 = k + 1 < norm.length ? norm[k + 1] : norm[0] + 2 * Math.PI, mid = (t0 + t1) / 2, [mx, my] = pt(c, mid);
        const other = circ.reduce((m, o, j) => m | ((j !== i && Math.hypot(mx - o.x, my - o.y) < o.r ? 1 : 0) << j), 0);
        arcs.push({ i, t0, t1, other });
      });
    });
    const f2 = (v) => Math.round(v * 100) / 100;
    const loopsFor = (mask) => {
      const mine = arcs.filter(a => (a.other | (1 << a.i)) === mask || a.other === mask).map(a => ({ ...a, p0: pt(circ[a.i], a.t0), p1: pt(circ[a.i], a.t1), used: false }));
      const near = (p, q) => Math.hypot(p[0] - q[0], p[1] - q[1]) < 0.5;
      let d = '';
      for (const start of mine) {
        if (start.used) continue;
        let a = start, fwd = true, first = true;
        while (a && !a.used) {
          a.used = true;
          const from = fwd ? a.p0 : a.p1, to = fwd ? a.p1 : a.p0, c = circ[a.i];
          if (first) { d += `M${f2(from[0])} ${f2(from[1])}`; first = false; }
          d += `A${c.r} ${c.r} 0 ${a.t1 - a.t0 > Math.PI ? 1 : 0} ${fwd ? 1 : 0} ${f2(to[0])} ${f2(to[1])}`;
          const nx = mine.find(b => !b.used && (near(b.p0, to) || near(b.p1, to)));
          if (nx) fwd = near(nx.p0, to);
          a = nx;
        }
        d += 'Z';
      }
      return d;
    };
    const rectPath = `M${rect.x} ${rect.y}h${rect.w}v${rect.h}h${-rect.w}Z`;

    /* Label positions: the point of each region farthest from every boundary */
    const best = {};
    for (let y = rect.y + 6; y < rect.y + rect.h - 6; y += 3) for (let x = rect.x + 6; x < rect.x + rect.w - 6; x += 3) {
      const m = maskAt(x, y); if (!m) continue;
      const clear = Math.min(...circ.map(c => Math.abs(Math.hypot(x - c.x, y - c.y) - c.r)));
      if (!best[m] || clear > best[m].c) best[m] = { x, y, c: clear };
    }

    const fr = C.frame(host, W, H, { label: P.label || `Venn diagram of ${sets.join(', ')}` });
    const g = fr.g;
    g.append(svg('rect', { class: 'cv-universe', x: rect.x, y: rect.y, width: rect.w, height: rect.h, rx: 12 }));
    const circG = svg('g', { class: 'cv-circles' }); circ.forEach((c, i) => circG.append(svg('circle', { class: 'cv-set cv-set-' + i, cx: c.x, cy: c.y, r: c.r })));
    const regG = svg('g', { class: 'cv-regions' }); g.append(regG, circG); // outlines above the region fills
    const labelOf = (i) => { const L = P.labels; return (Array.isArray(L) ? L[i] : L && L[sets[i]]) || sets[i]; };
    const regionName = (mask) => (mask ? (sets.filter((_, i) => mask >> i & 1).map((_, k, a) => a[k]).map(s => labelOf(sets.indexOf(s))).join(' and ') + (mask.toString(2).replace(/0/g, '').length < n ? ' only' : '')) : 'Outside every set');
    const regions = new Map();
    for (let mask = 0; mask < (1 << n); mask++) {
      const id = idOf(mask), d = mask ? loopsFor(mask) : rectPath + loopsFor(0);
      const pos = mask ? best[mask] : { x: rect.x + rect.w - 16, y: rect.y + rect.h - 18 };
      const val = svg('g', { class: 'cv-val' });
      const grp = svg('g', { class: 'cv-obj cv-region', 'data-id': id, 'data-tap': '', 'data-label': regionName(mask) }, [svg('path', { class: 'cv-body', d, 'fill-rule': 'evenodd' }), val]);
      regG.append(grp);
      regions.set(id, { grp, val, pos, mask });
    }
    /* Set labels outside the circles, universe label inside the top-left corner */
    const lab = svg('g', { class: 'cv-setlabels' }); g.append(lab);
    const at = n === 1 ? [-Math.PI * 0.75] : n === 2 ? [-Math.PI * 0.75, -Math.PI * 0.25] : [-Math.PI * 0.8, -Math.PI * 0.2, Math.PI * 0.72];
    circ.forEach((c, i) => {
      const t = at[i], [x, y] = pt({ ...c, r: c.r + 10 }, t);
      lab.append(C.label(x, y, labelOf(i), { anchor: Math.cos(t) < 0 ? 'end' : 'start', cls: 'cv-setname', size: 14, tex: /^\$.*\$$/.test(labelOf(i)) ? 'auto' : false }));
    });
    if (P.universe) lab.append(C.label(rect.x + 12, rect.y + 16, P.universe, { anchor: 'start', cls: 'cv-muted', tex: 'auto' }));

    const fmt = (v) => {
      if (v == null || v === '') return null;
      if (typeof v === 'number') return { text: P.mode === 'prob' ? C.fmtNum(v, 3) : C.fmtNum(v, 2), tex: false };
      const t = C.texOf(v); return { text: t.tex ? v : t.src, tex: t.tex };
    };
    let lastKey = '';
    const draw = (st) => {
      const sh = Array.isArray(st.shade) ? [st.shade] : Object.values(st.shade || {});
      const slot = new Map(); sh.forEach((list, k) => (list || []).forEach(id => { if (!slot.has(id)) slot.set(id, k + 1); }));
      const vals = { ...(P.values || {}), ...(st.values || {}) }, unknown = new Set(st.unknown || []), show = st.show !== false;
      const key = JSON.stringify([vals, [...unknown], show]);
      for (const [id, r] of regions) {
        for (let k = 1; k <= 6; k++) r.grp.classList.toggle('cv-sh' + k, slot.get(id) === k);
        r.grp.classList.toggle('is-shaded', slot.has(id));
        if (key !== lastKey) {
          r.val.replaceChildren();
          const v = unknown.has(id) ? { text: '?', tex: false } : fmt(vals[id]);
          if (v && show && r.pos) r.val.append(C.label(r.pos.x, r.pos.y + 0.5, v.text, { tex: v.tex ? 'auto' : false, size: 15, cls: 'cv-vtext', anchor: id === 'none' ? 'end' : 'middle', w: 70, h: 36 }));
        }
      }
      lastKey = key;
    };
    const I = C.instance({ kind: 'venn', factory: venn, params, ctx, fr, draw, defaults: { show: true } });
    I.api.regions = () => [...regions.keys()];
    I.api.set({}, { instant: true });
    return I.api;
  }

  C.register('venn', venn);
})();
