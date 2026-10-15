/* graph: nodes and edges (directed, weighted), visit order, current node, Markov chains with a distribution.
   Contract: docs/AUTHORING.md section 4; details in canvas/README-B.md. Builds on ZQ.cvb (canvas/plane.js). */
(function () {
  'use strict';
  const Z = window.ZQ;
  const C = Z.canvas;
  const { svg } = C;

  C.register('graph', (host, params, ctx) => {
    const K = Z.cvb;
    const W = 540, H = params.height || 300, r = params.nodeRadius || 22;
    const nodes = (params.nodes || []).map((n, i) => ({ ...n, id: n.id || 'n' + i }));
    const edges = (params.edges || []).map((e) => ({ ...e, directed: e.directed ?? params.directed ?? !!params.markov, id: e.id || `e-${e.from}-${e.to}` }));
    const padX = r + 26, padY = r + 22;
    const pos = (n) => [padX + (n.x ?? 0.5) * (W - 2 * padX), padY + (n.y ?? 0.5) * (H - 2 * padY)];
    const byId = Object.fromEntries(nodes.map((n) => [n.id, n]));
    const centre = nodes.length ? nodes.map(pos).reduce((a, p) => [a[0] + p[0] / nodes.length, a[1] + p[1] / nodes.length], [0, 0]) : [W / 2, H / 2];
    const wText = (e) => (e.label != null ? String(e.label) : e.w == null ? '' : params.markov ? K.fmt(e.w, 3) : K.fmt(e.w, 3));

    const def = {
      kind: 'graph', aria: params.aria || 'Graph',
      modes: ['tap'],
      size: () => ({ w: W, h: H }),
      skip: ['visited', 'current'],
      init: () => ({ visited: [], current: null, highlight: [], distribution: null, selected: [] }),
      alias: (id) => { const m = id.match(/^e-(.+?)-(.+)$/); if (!m) return [id]; const e = edges.find((q) => q.id === id || (!q.directed && q.from === m[2] && q.to === m[1])); return e ? [e.id] : [id]; },
      render(view, R) {
        const g = R.F.g, eg = svg('g'), ng = svg('g'), lg = svg('g'); g.append(eg, ng, lg);
        const visited = view.visited || [], dist = view.distribution || null;
        for (const e of edges) {
          const a = byId[e.from], b = byId[e.to]; if (!a || !b) continue;
          const [ax, ay] = pos(a), [bx, by] = pos(b);
          const o = K.obj(e.id, 'cvb-edge-o', e.colour || null);
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
            const s = [ax + r * Math.cos(sa), ay + r * Math.sin(sa)], t = [bx + (r + (e.directed ? 1 : 0)) * Math.cos(ea), by + (r + (e.directed ? 1 : 0)) * Math.sin(ea)];
            d = bend ? `M${s[0]},${s[1]}Q${2 * mx - (s[0] + t[0]) / 2},${2 * my - (s[1] + t[1]) / 2} ${t[0]},${t[1]}` : `M${s[0]},${s[1]}L${t[0]},${t[1]}`;
            lx = mx + nx * (bend ? 8 : 0); ly = my + ny * (bend ? 8 : 0); hx = t[0]; hy = t[1];
            tx = t[0] - (bend ? 2 * mx - (s[0] + t[0]) / 2 : s[0]); ty = t[1] - (bend ? 2 * my - (s[1] + t[1]) / 2 : s[1]);
          }
          o.append(K.washPath(d), svg('path', { d, class: 'cvb-edge' + (e.dashed ? ' cvb-dash' : '') }));
          if (e.directed) { const L = Math.hypot(tx, ty) || 1, ux = tx / L, uy = ty / L, s = 9; o.append(svg('path', { d: `M${hx},${hy}L${hx - ux * s - uy * s * 0.5},${hy - uy * s + ux * s * 0.5}L${hx - ux * s + uy * s * 0.5},${hy - uy * s - ux * s * 0.5}Z`, class: 'cvb-head', style: 'fill: var(--c, var(--text-2))' })); }
          eg.append(o);
          const wt = view.show === 'none' ? '' : wText(e);
          if (wt) {
            const w = K.tw(wt, 12) + 10;
            const lgp = svg('g', { class: 'cv-obj', 'data-id': 'w-' + e.id });
            lgp.append(svg('rect', { x: lx - w / 2, y: ly - 10, width: w, height: 20, rx: 10, class: 'cvb-wpill' }), K.txt(lx, ly, wt, { size: 12, weight: 600 }));
            lg.append(lgp);
          }
        }
        const sel = new Set(view.selected || []);
        for (const n of nodes) {
          const [x, y] = pos(n), o = K.obj(n.id, 'cvb-node-o' + (sel.has(n.id) ? ' is-on' : ''), n.colour || null);
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
          o.append(K.lab(x, y, n.label ?? n.id, { w: r * 2 + 20, size: 14 }));
          if (vi >= 0 && view.order !== false) {
            const bx = x + r * 0.78, by = y - r * 0.78;
            o.append(svg('circle', { cx: bx, cy: by, r: 9, class: 'cvb-visit' }), K.txt(bx, by + 0.5, String(vi + 1), { cls: 'cvb-visit-t', size: 11 }));
          }
          R.tappable(o, n.id, 'Node ' + (n.label ?? n.id));
          ng.append(o);
        }
      },
    };
    return K.make(host, params, ctx, def);
  });
})();
