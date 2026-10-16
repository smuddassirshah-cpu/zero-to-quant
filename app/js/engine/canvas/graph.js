/* graph: nodes and edges (directed, weighted), visit order, current node, Markov chains with a distribution.
   Contract: docs/AUTHORING.md section 4; details in canvas/README-B.md. Builds on ZQ.cvb (canvas/plane.js).
   Nodes and edges live in state (seeded from params), so a patch can add, move or remove them: a list replaces,
   a map keyed by id merges, adds (a new id) or removes (null); nodes and edges fade and grow in or out. layout:
   "ring" seats the nodes evenly round a circle and state.rotate turns them (in seats). state.labels relabels nodes.
   Without nodeRadius, the radius grows to the longest label (up to 34) and longer labels shrink to fit. */
(function () {
  'use strict';
  const Z = window.ZQ;
  const C = Z.canvas;
  const { svg } = C;

  C.register('graph', (host, params, ctx) => {
    const K = Z.cvb;
    const W = 540, H = params.height || 300, ring = params.layout === 'ring';
    const normNodes = (list) => (list || []).filter(Boolean).map((n, i) => ({ ...n, id: String(n.id ?? 'n' + i) }));
    const normEdges = (list) => (list || []).filter((e) => e && e.from != null && e.to != null).map((e) => ({ ...e, from: String(e.from), to: String(e.to), id: e.id || `e-${e.from}-${e.to}` }));
    const isDir = (e) => e.directed ?? params.directed ?? !!params.markov;
    const nodes0 = normNodes(params.nodes);
    /* item 99: the radius fits the longest label (from 22 up to 34) unless nodeRadius is given; longer labels shrink */
    const labOf = (n, view) => String((view && view.labels && view.labels[n.id] != null ? view.labels[n.id] : n.label) ?? n.id);
    const plainW = (t, size) => K.tw(String(t).replace(/\$|\\[a-zA-Z]+|[{}^_]/g, ''), size);
    const initLabels = (params.state && params.state.labels) || {};
    const r = params.nodeRadius || Math.round(K.clamp(Math.max(0, ...nodes0.map((n) => plainW(initLabels[n.id] ?? n.label ?? n.id, 14))) / 2 + 8, 22, 34));
    const labSize = (t) => { const w = plainW(t, 14); return w <= 2 * r - 8 ? 14 : Math.max(10, Math.floor(14 * (2 * r - 8) / w)); };
    const padX = r + 26, padY = r + 22;
    const ringR = Math.max(40, Math.min(W / 2 - padX, H / 2 - padY));
    const pos = (n, view) => {
      if (ring && n.a != null) { const t = 2 * Math.PI * (n.a + ((view && view.rotate) || 0) / Math.max(1, view && view.seats ? view.seats : 1)) - Math.PI / 2; return [W / 2 + ringR * Math.cos(t), H / 2 + ringR * Math.sin(t)]; }
      return [padX + (n.x ?? 0.5) * (W - 2 * padX), padY + (n.y ?? 0.5) * (H - 2 * padY)];
    };
    const wText = (e) => (e.label != null ? String(e.label) : e.w == null ? '' : params.markov ? K.fmt(e.w, 3) : K.fmt(e.w, 3));
    /* ring seats: a = fraction of a turn for each live node, in list order; seats = how many there are */
    const seat = (list) => { const live = list.filter((n) => !n.gone); return live.map((n, k) => ({ ...n, a: k / Math.max(1, live.length) })); };
    /* a list replaces; a map merges by id, adds new ids, removes ids set to null */
    const applyList = (cur, patch, norm) => {
      if (Array.isArray(patch)) return norm(patch);
      if (!K.isObj(patch)) return cur;
      const out = cur.filter((it) => patch[it.id] !== null).map((it) => (K.isObj(patch[it.id]) ? { ...it, ...patch[it.id] } : it));
      Object.entries(patch).forEach(([id, v]) => { if (K.isObj(v) && !cur.some((it) => it.id === id)) out.push(...norm([{ id, ...v }])); });
      return out;
    };

    const def = {
      kind: 'graph', aria: params.aria || 'Graph',
      modes: ['tap'],
      size: () => ({ w: W, h: H }),
      skip: ['visited', 'current', 'labels', 'gone'],
      init: () => {
        const nodes = ring ? seat(nodes0) : nodes0;
        return { nodes, edges: normEdges(params.edges), rotate: 0, seats: nodes.length, labels: {}, visited: [], current: null, highlight: [], distribution: null, selected: [] };
      },
      prepare(patch, state) {
        if ('nodes' in patch) {
          let nodes = applyList(state.nodes || [], patch.nodes, normNodes);
          if (ring) nodes = seat(nodes);
          patch.nodes = nodes;
          if (ring) patch.seats = nodes.length;
          const ids = new Set(nodes.map((n) => n.id));
          const edges = 'edges' in patch ? applyList(state.edges || [], patch.edges, normEdges) : state.edges || [];
          patch.edges = edges.filter((e) => ids.has(e.from) && ids.has(e.to));
        } else if ('edges' in patch) patch.edges = applyList(state.edges || [], patch.edges, normEdges);
        return patch;
      },
      /* nodes and edges that arrive fade and grow in; those that leave fade out where they were */
      animate(prev, next, { instant, alive, show }) {
        if (instant) { show(next); return; }
        const join = (a, b) => {
          const A = (a || []).map((it) => ({ o: 1, ...it })), B = (b || []).map((it) => ({ o: 1, ...it }));
          const from = [...A], to = [...B];
          B.forEach((it) => { if (!A.some((x) => x.id === it.id)) from.push({ ...it, o: 0 }); });
          A.forEach((it) => { if (!B.some((x) => x.id === it.id)) to.push({ ...it, o: 0, gone: true }); });
          to.sort((x, y) => from.findIndex((q) => q.id === x.id) - from.findIndex((q) => q.id === y.id));
          return [from, to];
        };
        const [nf, nt] = join(prev.nodes, next.nodes), [ef, et] = join(prev.edges, next.edges);
        const from = { ...prev, nodes: nf, edges: ef }, to = { ...next, nodes: nt, edges: et };
        const ms = 600;
        return C.tween(0, 1, ms, (t) => { if (!alive()) return; show(t >= 1 ? next : K.lerp(from, to, t, def.skip)); });
      },
      alias: (id, R) => { const m = id.match(/^e-(.+?)-(.+)$/); if (!m) return [id]; const e = ((R && R.state.edges) || []).find((q) => q.id === id || (!isDir(q) && q.from === m[2] && q.to === m[1])); return e ? [e.id] : [id]; },
      render(view, R) {
        const g = R.F.g, eg = svg('g'), ng = svg('g'), lg = svg('g'); g.append(eg, ng, lg);
        const visited = view.visited || [], dist = view.distribution || null;
        const nodes = view.nodes || [], edges = view.edges || [];
        const byId = Object.fromEntries(nodes.map((n) => [n.id, n]));
        const live = nodes.filter((n) => !n.gone);
        const centre = live.length ? live.map((n) => pos(n, view)).reduce((a, p) => [a[0] + p[0] / live.length, a[1] + p[1] / live.length], [0, 0]) : [W / 2, H / 2];
        const fade = (o, v) => { if (v != null && v < 1) o.setAttribute('opacity', Math.max(0, v).toFixed(3)); return o; };
        for (const e of edges) {
          const a = byId[e.from], b = byId[e.to]; if (!a || !b) continue;
          const [ax, ay] = pos(a, view), [bx, by] = pos(b, view);
          const directed = isDir(e);
          const o = fade(K.obj(e.id, 'cvb-edge-o', e.colour || null), Math.min(e.o ?? 1, a.o ?? 1, b.o ?? 1));
          let d, lx, ly, hx, hy, tx, ty;
          if (e.from === e.to) {
            const dcx = ax - centre[0], dcy = ay - centre[1], ang = Math.hypot(dcx, dcy) < 1 ? -Math.PI / 2 : Math.atan2(dcy, dcx), ux = Math.cos(ang), uy = Math.sin(ang);
            const p1 = [ax + r * Math.cos(ang - 0.5), ay + r * Math.sin(ang - 0.5)], p2 = [ax + r * Math.cos(ang + 0.5), ay + r * Math.sin(ang + 0.5)];
            const c1 = [ax + (r + 42) * Math.cos(ang - 0.7), ay + (r + 42) * Math.sin(ang - 0.7)], c2 = [ax + (r + 42) * Math.cos(ang + 0.7), ay + (r + 42) * Math.sin(ang + 0.7)];
            d = `M${p1[0]},${p1[1]}C${c1[0]},${c1[1]} ${c2[0]},${c2[1]} ${p2[0]},${p2[1]}`;
            lx = ax + ux * (r + 40); ly = ay + uy * (r + 40); hx = p2[0]; hy = p2[1]; tx = p2[0] - c2[0]; ty = p2[1] - c2[1];
          } else {
            const both = edges.some((q) => q !== e && q.from === e.to && q.to === e.from);
            const dx = bx - ax, dy = by - ay, L = Math.hypot(dx, dy) || 1, ux = dx / L, uy = dy / L, nx = -uy, ny = ux;
            const bend = both ? 22 : (e.bend || 0);
            const mx = (ax + bx) / 2 + nx * bend, my = (ay + by) / 2 + ny * bend;
            const sa = Math.atan2(my - ay, mx - ax), ea = Math.atan2(my - by, mx - bx);
            const s = [ax + r * Math.cos(sa), ay + r * Math.sin(sa)], t = [bx + (r + (directed ? 1 : 0)) * Math.cos(ea), by + (r + (directed ? 1 : 0)) * Math.sin(ea)];
            d = bend ? `M${s[0]},${s[1]}Q${2 * mx - (s[0] + t[0]) / 2},${2 * my - (s[1] + t[1]) / 2} ${t[0]},${t[1]}` : `M${s[0]},${s[1]}L${t[0]},${t[1]}`;
            lx = mx + nx * (bend ? 8 : 0); ly = my + ny * (bend ? 8 : 0); hx = t[0]; hy = t[1];
            tx = t[0] - (bend ? 2 * mx - (s[0] + t[0]) / 2 : s[0]); ty = t[1] - (bend ? 2 * my - (s[1] + t[1]) / 2 : s[1]);
          }
          o.append(K.washPath(d), svg('path', { d, class: 'cvb-edge' + (e.dashed ? ' cvb-dash' : '') }));
          if (directed) { const L = Math.hypot(tx, ty) || 1, ux = tx / L, uy = ty / L, s = 9; o.append(svg('path', { d: `M${hx},${hy}L${hx - ux * s - uy * s * 0.5},${hy - uy * s + ux * s * 0.5}L${hx - ux * s + uy * s * 0.5},${hy - uy * s - ux * s * 0.5}Z`, class: 'cvb-head', style: 'fill: var(--c, var(--text-2))' })); }
          eg.append(o);
          const wt = view.show === 'none' ? '' : wText(e);
          if (wt) {
            const w = K.tw(wt, 12) + 10;
            const lgp = fade(svg('g', { class: 'cv-obj', 'data-id': 'w-' + e.id }), Math.min(e.o ?? 1, a.o ?? 1, b.o ?? 1));
            lgp.append(svg('rect', { x: lx - w / 2, y: ly - 10, width: w, height: 20, rx: 10, class: 'cvb-wpill' }), K.txt(lx, ly, wt, { size: 12, weight: 600 }));
            lg.append(lgp);
          }
        }
        const sel = new Set(view.selected || []);
        for (const n of nodes) {
          const [x, y] = pos(n, view), o = K.obj(n.id, 'cvb-node-o' + (sel.has(n.id) ? ' is-on' : ''), n.colour || null);
          if ((n.o ?? 1) < 1) { fade(o, n.o); const k = 0.6 + 0.4 * Math.max(0, n.o); o.setAttribute('transform', `translate(${x} ${y}) scale(${k.toFixed(3)}) translate(${-x} ${-y})`); }
          o.append(K.washCircle(x, y, r + 8));
          if (view.current === n.id) o.append(svg('circle', { cx: x, cy: y, r: r + 5, class: 'cvb-ln', style: 'stroke: var(--manip); stroke-width: 3' }));
          o.append(svg('circle', { cx: x, cy: y, r, class: 'cvb-node cvb-tapbox cv-body' + (view.current === n.id ? ' cur' : '') }));
          const vi = visited.indexOf(n.id);
          if (vi >= 0) o.append(svg('circle', { cx: x, cy: y, r: r - 1, class: 'cvb-node-fill', style: 'fill-opacity: 0.14' }));
          if (dist && dist[n.id] != null) {
            const p = K.clamp(+dist[n.id], 0, 1), cid = R.uid + '-nc-' + n.id;
            let cp = R.defs.querySelector('#' + CSS.escape(cid)); if (!cp) { cp = svg('clipPath', { id: cid }, [svg('circle')]); R.defs.append(cp); }
            C.attrs(cp.firstChild, { cx: x, cy: y, r: r - 1.5 });
            o.append(svg('rect', { x: x - r, y: y + r - 2 * r * p, width: 2 * r, height: 2 * r * p, class: 'cvb-node-fill', 'clip-path': `url(#${cid})` }));
            o.append(K.txt(x, y + r + 12, K.fmt(p, 3), { size: 12, weight: 600, halo: true, cls: 'cvb-outink' }));
          }
          const lt = labOf(n, view);
          o.append(K.lab(x, y, lt, { w: r * 2 + 20, size: labSize(lt) }));
          if (vi >= 0 && view.order !== false) {
            const bx = x + r * 0.78, by = y - r * 0.78;
            o.append(svg('circle', { cx: bx, cy: by, r: 9, class: 'cvb-visit' }), K.txt(bx, by + 0.5, String(vi + 1), { cls: 'cvb-visit-t', size: 11 }));
          }
          if (!n.gone) R.tappable(o, n.id, 'Node ' + lt);
          ng.append(o);
        }
      },
    };
    return K.make(host, params, ctx, def);
  });
})();
