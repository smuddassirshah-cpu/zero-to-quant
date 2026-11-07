/* graph: nodes and edges (directed, weighted), visit order, current node, Markov chains with a distribution.
   Contract: docs/AUTHORING.md section 4; details in canvas/README-B.md. Builds on ZQ.cvb (canvas/plane.js).
   Nodes and edges live in state (seeded from params), so a patch can add, move or remove them: a list replaces,
   a map keyed by id merges, adds (a new id) or removes (null); nodes and edges fade and grow in or out. layout:
   "ring" seats the nodes evenly round a circle and state.rotate turns them (in seats). state.labels relabels nodes.
   Without nodeRadius, the radius grows to the longest label (up to 34) and longer labels shrink to fit.
   Pass 7: the radius follows labels set later too (item 416), the frame padding follows the nodes' own extents
   (item 439), edge labels may hold KaTeX, state.pointers names nodes (slow, fast) with labelled arrows (item 406),
   state.values writes a value under a node, and params.lattice lays out a recombining binomial lattice (items 374, 444). */
(function () {
  'use strict';
  const Z = window.ZQ;
  const C = Z.canvas;
  const { svg } = C;

  C.register('graph', (host, params, ctx) => {
    const K = Z.cvb;
    let fitWatch = null;
    let W = 540; const ring = params.layout === 'ring';
    /* items 374, 444: lattice: { steps: n, S0, u, d, decimals, money, labels, stepLabels } generates nodes n{t}_{k} (k up
       moves after t steps) at x = t / n, recombining, with edges to n{t+1}_{k+1} (up) and n{t+1}_{k} (down) */
    const lat = params.lattice && typeof params.lattice === 'object' ? params.lattice : null;
    const latSteps = lat ? Math.max(1, Math.min(8, Math.round(+lat.steps || 2))) : 0;
    const latNodes = () => {
      const out = [], L = lat.labels || {}, dp = lat.decimals ?? 2;
      for (let t = 0; t <= latSteps; t++) for (let k = 0; k <= t; k++) {
        const id = `n${t}_${k}`, price = lat.S0 != null ? +lat.S0 * Math.pow(+(lat.u ?? 1.1), k) * Math.pow(+(lat.d ?? 1 / +(lat.u ?? 1.1)), t - k) : null;
        const text = L[id] != null ? String(L[id]) : price != null ? (lat.money || '') + price.toFixed(dp) : `${k}u ${t - k}d`;
        out.push({ id, label: text, x: t / latSteps, y: 0.5 - (2 * k - t) / (2 * latSteps), shape: lat.shape || 'rect' });
      }
      return out;
    };
    const latEdges = () => { const out = []; for (let t = 0; t < latSteps; t++) for (let k = 0; k <= t; k++) { out.push({ from: `n${t}_${k}`, to: `n${t + 1}_${k + 1}` }, { from: `n${t}_${k}`, to: `n${t + 1}_${k}` }); } return out; };
    const H = params.height || (lat ? Math.max(240, 70 * latSteps + 90) : 300);
    const normNodes = (list) => (list || []).filter(Boolean).map((n, i) => ({ ...n, id: String(n.id ?? 'n' + i) }));
    const normEdges = (list) => (list || []).filter((e) => e && e.from != null && e.to != null).map((e) => ({ ...e, from: String(e.from), to: String(e.to), id: e.id || `e-${e.from}-${e.to}` }));
    const isDir = (e) => e.directed ?? params.directed ?? !!params.markov;
    const nodes0 = normNodes(lat ? [...latNodes(), ...(params.nodes || [])] : params.nodes);
    /* item 99: the radius fits the longest label (from 22 up to 34) unless nodeRadius is given; longer labels shrink */
    const labOf = (n, view) => String((view && view.labels && view.labels[n.id] != null ? view.labels[n.id] : n.label) ?? n.id);
    const plainW = (t, size) => K.tw(String(t).replace(/\$|\\[a-zA-Z]+|[{}^_]/g, ''), size);
    const initLabels = (params.state && params.state.labels) || {};
    const fitR = (list, labels) => Math.round(K.clamp(Math.max(0, ...list.flatMap((n) => String((labels || {})[n.id] ?? n.label ?? n.id).split('\n').map((l) => plainW(l, 14)))) / 2 + 8, 22, 34));
    const r0 = params.nodeRadius || fitR(nodes0, initLabels);
    let r = r0, padX = r + 26, padY = r + 22, small = false, capHw = {};
    /* item 152: a node may carry its own r, and shape: "pill" (a rounded box as wide as its label); edges stop at the rim */
    /* item 117: also shape "rect" (a rounded box sized to the label, multi-line labels too) and "diamond" */
    const widest = (t) => Math.max(...String(t).split('\n').map(l => plainW(l, small ? 12 : 14)));
    const shapeOf = (n, view) => {
      const rr = n.r || r, lt = labOf(n, view), nl = String(lt).split('\n').length, cap = capHw[n.id] ?? Infinity;
      if (n.shape === 'pill') return { kind: 'pill', pill: true, hw: Math.min(Math.max(rr, widest(lt) / 2 + 12), cap), hh: Math.max(Math.min(rr, 18), nl * 9 + 4), rr };
      if (n.shape === 'rect') return { kind: 'rect', pill: true, hw: Math.min(Math.max(rr, widest(lt) / 2 + 10), cap), hh: Math.max(Math.min(rr, 18), nl * 9 + 6), rr };
      if (n.shape === 'diamond') return { kind: 'diamond', pill: false, hw: rr * 1.3, hh: rr * 1.3, rr };
      return { kind: 'circle', pill: false, hw: rr, hh: rr, rr };
    };
    const rimAt = (sh, ang) => {
      const c = Math.abs(Math.cos(ang)), si = Math.abs(Math.sin(ang));
      if (sh.kind === 'diamond') return 1 / (c / sh.hw + si / sh.hh);
      if (!sh.pill) return sh.hw;
      return Math.min(c > 1e-6 ? sh.hw / c : Infinity, si > 1e-6 ? sh.hh / si : Infinity);
    };
    /* item 165: plain labels never shrink below 12px; a long one wraps onto two lines at a space, then truncates with … */
    const nodeLabel = (x, y, lt, maxW) => {
      lt = String(lt);
      if (lt.includes('$')) return K.lab(x, y, lt, { w: maxW + 20, size: 14 });
      let lines = lt.split('\n'), size = small ? 12 : 14;
      while (size > 12 && lines.some(l => plainW(l, size) > maxW)) size--;
      if (lines.length === 1 && plainW(lines[0], size) > maxW && lines[0].includes(' ')) {
        const words = lines[0].split(' '); let best = null;
        for (let k = 1; k < words.length; k++) { const a = words.slice(0, k).join(' '), b = words.slice(k).join(' '), m = Math.max(plainW(a, size), plainW(b, size)); if (!best || m < best.m) best = { a, b, m }; }
        lines = [best.a, best.b];
      }
      const cut = (l) => { if (plainW(l, size) <= maxW) return l; let t = l; while (t.length > 1 && plainW(t + '…', size) > maxW) t = t.slice(0, -1); return t + '…'; };
      lines = lines.map(cut);
      const g = svg('g'), lh = size + 2, y0 = y - (lines.length - 1) * lh / 2;
      lines.forEach((l, k) => g.append(K.txt(x, y0 + k * lh, l, { size })));
      return g;
    };
    let ringR = Math.max(40, Math.min(W / 2 - padX, H / 2 - padY));
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
      skip: ['visited', 'current', 'labels', 'gone', 'values', 'pointers'],
      init: () => {
        const nodes = ring ? seat(nodes0) : nodes0;
        return { nodes, edges: normEdges(lat ? [...latEdges(), ...(params.edges || [])] : params.edges), rotate: 0, seats: nodes.length, labels: {}, visited: [], current: null, highlight: [], distribution: null, selected: [] };
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
        /* item 333: on a narrow column the frame narrows to the column (down to 300 wide) instead of shrinking the
           drawing, so node labels keep their 12px minimum on a phone; the layout re-spaces to fit */
        if (!fitWatch && !R.static && typeof ResizeObserver === 'function' && params.fitWidth !== false) {
          fitWatch = new ResizeObserver(() => { const w = Math.round(R.F.wrap.clientWidth || 0); if (!w) return; const nw = Math.max(300, Math.min(540, w)); if (nw !== W) { W = nw; ringR = Math.max(40, Math.min(W / 2 - padX, H / 2 - padY)); R.F.resize(W, H); R.redraw(); } });
          fitWatch.observe(R.F.wrap);
        }
        /* item 416: a label set later can widen the circles (never below the opening radius); item 439: the padding is
           the nodes' own half-size plus a margin, so rect and pill nodes neither waste the frame nor run off its edge;
           item 399: below 440px pills and rects size their text at 12px */
        small = W < 440;
        if (!params.nodeRadius) r = Math.max(r0, fitR(view.nodes || [], view.labels));
        const layoutPad = () => { const ext = (view.nodes || []).filter((n) => !n.gone).map((n) => shapeOf(n, view)); const mw = Math.max(r, ...ext.map((q) => q.hw)), mh = Math.max(14, ...ext.map((q) => q.hh)); padX = mw + 26; padY = mh + 22 + (lat && lat.stepLabels ? 14 : 0); ringR = Math.max(40, Math.min(W / 2 - padX, H / 2 - padY)); };
        capHw = {}; layoutPad();
        /* ENGINE-BACKLOG 609: on a phone a row of rect or pill nodes keeps its desktop widths and the boxes touch, so the edges between
           neighbours vanish. A rect or pill is capped at half the distance to its nearest neighbour in the row, less a 5px gap (never
           under 20px); its label then wraps or truncates inside the box as it already does. Two passes: the cap moves the padding. */
        if (small) for (let pass = 0; pass < 2; pass++) {
          const live0 = (view.nodes || []).filter((n) => !n.gone), sh0 = new Map(live0.map((n) => [n.id, shapeOf(n, view)])), p0 = new Map(live0.map((n) => [n.id, pos(n, view)]));
          capHw = {};
          for (const a of live0) {
            const sa = sh0.get(a.id); if (!sa.pill) continue;
            let near = Infinity;
            for (const b of live0) { if (b === a) continue; const [ax, ay] = p0.get(a.id), [bx, by] = p0.get(b.id), sb = sh0.get(b.id); if (Math.abs(ay - by) < sa.hh + sb.hh) near = Math.min(near, Math.abs(ax - bx)); }
            if (near < Infinity) capHw[a.id] = Math.max(20, near / 2 - 5);
          }
          layoutPad();
        }
        const g = R.F.g, eg = svg('g'), ng = svg('g'), lg = svg('g'); g.append(eg, ng, lg);
        /* lattice step labels along the bottom (t = 0, 1, ...; stepLabels: true or a list) */
        if (lat && lat.stepLabels) { const sl = Array.isArray(lat.stepLabels) ? lat.stepLabels : Array.from({ length: latSteps + 1 }, (_, t) => 't = ' + t); sl.forEach((t, k) => { if (t == null || t === '' || k > latSteps) return; const x = padX + (k / latSteps) * (W - 2 * padX); g.append(String(t).includes('$') ? K.lab(x, H - 12, String(t), { size: 12, cls: 'cvb-muted' }) : K.txt(x, H - 12, String(t), { size: 12, cls: 'cvb-muted' })); }); }
        /* lanes (item 149): labelled horizontal bands behind the graph, such as "local" and "origin" for commits */
        if (Array.isArray(params.lanes) && params.lanes.length) {
          const lanesG = svg('g', { class: 'cvb-lanes' });
          params.lanes.forEach((l) => {
            const ly = padY + (+l.y || 0) * (H - 2 * padY);
            lanesG.append(svg('line', { x1: 8, x2: W - 8, y1: ly, y2: ly, class: 'cvb-lane' }));
            if (l.label) lanesG.append(K.txt(10, ly - r - 8, String(l.label), { anchor: 'start', size: 12, weight: 600, cls: 'cvb-muted' }));
          });
          g.insertBefore(lanesG, eg);
        }
        const visited = view.visited || [], dist = view.distribution || null;
        const nodes = view.nodes || [], edges = view.edges || [];
        const byId = Object.fromEntries(nodes.map((n) => [n.id, n]));
        const live = nodes.filter((n) => !n.gone);
        const centre = live.length ? live.map((n) => pos(n, view)).reduce((a, p) => [a[0] + p[0] / live.length, a[1] + p[1] / live.length], [0, 0]) : [W / 2, H / 2];
        const fade = (o, v) => { if (v != null && v < 1) o.setAttribute('opacity', Math.max(0, v).toFixed(3)); return o; };
        for (const e of edges) {
          const a = byId[e.from], b = byId[e.to]; if (!a || !b) continue;
          const [ax, ay] = pos(a, view), [bx, by] = pos(b, view);
          const directed = isDir(e), shA = shapeOf(a, view), shB = shapeOf(b, view);
          const o = fade(K.obj(e.id, 'cvb-edge-o', e.colour || null), Math.min(e.o ?? 1, a.o ?? 1, b.o ?? 1));
          let d, lx, ly, hx, hy, tx, ty;
          if (e.from === e.to) {
            /* item 312: loopAngle (degrees, 0 is right, 90 is up) points a self-loop that way; by default it points away
               from the centre of the graph */
            const dcx = ax - centre[0], dcy = ay - centre[1], ang = e.loopAngle != null && Number.isFinite(+e.loopAngle) ? -(+e.loopAngle) * Math.PI / 180 : Math.hypot(dcx, dcy) < 1 ? -Math.PI / 2 : Math.atan2(dcy, dcx), ux = Math.cos(ang), uy = Math.sin(ang);
            const r1 = rimAt(shA, ang - 0.5), r2 = rimAt(shA, ang + 0.5), rm = rimAt(shA, ang);
            const p1 = [ax + r1 * Math.cos(ang - 0.5), ay + r1 * Math.sin(ang - 0.5)], p2 = [ax + r2 * Math.cos(ang + 0.5), ay + r2 * Math.sin(ang + 0.5)];
            const c1 = [ax + (rm + 42) * Math.cos(ang - 0.7), ay + (rm + 42) * Math.sin(ang - 0.7)], c2 = [ax + (rm + 42) * Math.cos(ang + 0.7), ay + (rm + 42) * Math.sin(ang + 0.7)];
            d = `M${p1[0]},${p1[1]}C${c1[0]},${c1[1]} ${c2[0]},${c2[1]} ${p2[0]},${p2[1]}`;
            lx = ax + ux * (rm + 40); ly = ay + uy * (rm + 40); hx = p2[0]; hy = p2[1]; tx = p2[0] - c2[0]; ty = p2[1] - c2[1];
          } else {
            const both = edges.some((q) => q !== e && q.from === e.to && q.to === e.from);
            const dx = bx - ax, dy = by - ay, L = Math.hypot(dx, dy) || 1, ux = dx / L, uy = dy / L, nx = -uy, ny = ux;
            const bend = both ? 22 : (e.bend || 0);
            const mx = (ax + bx) / 2 + nx * bend, my = (ay + by) / 2 + ny * bend;
            const sa = Math.atan2(my - ay, mx - ax), ea = Math.atan2(my - by, mx - bx);
            const ra = rimAt(shA, sa), rb = rimAt(shB, ea) + (directed ? 1 : 0);
            const s = [ax + ra * Math.cos(sa), ay + ra * Math.sin(sa)], t = [bx + rb * Math.cos(ea), by + rb * Math.sin(ea)];
            d = bend ? `M${s[0]},${s[1]}Q${2 * mx - (s[0] + t[0]) / 2},${2 * my - (s[1] + t[1]) / 2} ${t[0]},${t[1]}` : `M${s[0]},${s[1]}L${t[0]},${t[1]}`;
            lx = mx + nx * (bend ? 8 : 0); ly = my + ny * (bend ? 8 : 0); hx = t[0]; hy = t[1];
            tx = t[0] - (bend ? 2 * mx - (s[0] + t[0]) / 2 : s[0]); ty = t[1] - (bend ? 2 * my - (s[1] + t[1]) / 2 : s[1]);
          }
          o.append(K.washPath(d), svg('path', { d, class: 'cvb-edge' + (e.dashed ? ' cvb-dash' : '') }));
          /* item 117: edges are tappable in tap mode with params.tapEdges, or when the widget's ids name them */
          if (R.mode === 'tap' && (params.tapEdges || (R.modeOpts.only && R.modeOpts.only.includes(e.id)))) { o.append(svg('path', { d, class: 'cvb-tapbox cv-body', style: 'stroke: transparent; stroke-width: 20px; fill: none' })); R.tappable(o, e.id, `Edge from ${labOf(a, view)} to ${labOf(b, view)}`.replace(/\n/g, ' ')); }
          if (directed) { const L = Math.hypot(tx, ty) || 1, ux = tx / L, uy = ty / L, s = 9; o.append(svg('path', { d: `M${hx},${hy}L${hx - ux * s - uy * s * 0.5},${hy - uy * s + ux * s * 0.5}L${hx - ux * s + uy * s * 0.5},${hy - uy * s - ux * s * 0.5}Z`, class: 'cvb-head', style: 'fill: var(--c, var(--text-2))' })); }
          eg.append(o);
          const wt = view.show === 'none' ? '' : wText(e);
          if (wt) {
            const tex = /\$/.test(wt), w = K.tw(tex ? wt.replace(/\$|\\[a-zA-Z]+|[{}^_]/g, '') : wt, 12) + (tex ? 14 : 10);
            const lgp = fade(svg('g', { class: 'cv-obj', 'data-id': 'w-' + e.id }), Math.min(e.o ?? 1, a.o ?? 1, b.o ?? 1));
            /* item 416: an edge label may hold KaTeX ("$\\lambda$", "$w = 2$") */
            lgp.append(svg('rect', { x: lx - w / 2, y: ly - 10, width: w, height: 20, rx: 10, class: 'cvb-wpill' }), tex ? K.lab(lx, ly, wt, { w: w + 8, h: 20, size: 12 }) : K.txt(lx, ly, wt, { size: 12, weight: 600 }));
            lg.append(lgp);
          }
        }
        const sel = new Set(view.selected || []);
        for (const n of nodes) {
          const [x, y] = pos(n, view), o = K.obj(n.id, 'cvb-node-o' + (sel.has(n.id) ? ' is-on' : ''), n.colour || null);
          if ((n.o ?? 1) < 1) { fade(o, n.o); const k = 0.6 + 0.4 * Math.max(0, n.o); o.setAttribute('transform', `translate(${x} ${y}) scale(${k.toFixed(3)}) translate(${-x} ${-y})`); }
          const sh = shapeOf(n, view), { hw, hh } = sh;
          /* the node's outline: a circle, or a pill; dashed: true draws it dashed (item 149) */
          const shape = (grow, attrs) => (sh.kind === 'diamond' ? svg('path', { d: `M${x},${y - hh - grow * 1.4}L${x + hw + grow * 1.4},${y}L${x},${y + hh + grow * 1.4}L${x - hw - grow * 1.4},${y}Z`, ...attrs })
            : sh.pill ? svg('rect', { x: x - hw - grow, y: y - hh - grow, width: 2 * (hw + grow), height: 2 * (hh + grow), rx: sh.kind === 'rect' ? 6 + Math.max(0, grow) : hh + grow, ...attrs }) : svg('circle', { cx: x, cy: y, r: hw + grow, ...attrs }));
          o.append(sh.kind === 'circle' ? K.washCircle(x, y, hw + 8) : shape(8, { class: 'cvb-hlw' }));
          if (view.current === n.id) o.append(shape(5, { class: 'cvb-ln', style: 'stroke: var(--manip); stroke-width: 3' }));
          o.append(shape(0, { class: 'cvb-node cvb-tapbox cv-body' + (view.current === n.id ? ' cur' : '') + (n.dashed ? ' cvb-dash' : '') }));
          const vi = visited.indexOf(n.id);
          if (vi >= 0) o.append(shape(-1, { class: 'cvb-node-fill', style: 'fill-opacity: 0.14' }));
          if (dist && dist[n.id] != null) {
            const p = K.clamp(+dist[n.id], 0, 1), cid = R.uid + '-nc-' + n.id;
            let cp = R.defs.querySelector('#' + CSS.escape(cid)); if (!cp) { cp = svg('clipPath', { id: cid }); R.defs.append(cp); }
            cp.replaceChildren(shape(-1.5, {}));
            o.append(svg('rect', { x: x - hw, y: y + hh - 2 * hh * p, width: 2 * hw, height: 2 * hh * p, class: 'cvb-node-fill', 'clip-path': `url(#${cid})` }));
            /* item 314: valueSide on a node ("below" default, "above", "left", "right") moves its distribution value clear of a loop */
            const vs = n.valueSide || (view.valueSide || {})[n.id] || 'below';
            const [vx, vy, va] = vs === 'above' ? [x, y - hh - 12, 'middle'] : vs === 'left' ? [x - hw - 6, y, 'end'] : vs === 'right' ? [x + hw + 6, y, 'start'] : [x, y + hh + 12, 'middle'];
            o.append(K.txt(vx, vy, K.fmt(p, 3), { size: 12, weight: 600, halo: true, cls: 'cvb-outink', anchor: va }));
          }
          const lt = labOf(n, view);
          o.append(nodeLabel(x, y, lt, sh.pill ? 2 * hw - (capHw[n.id] != null && hw <= capHw[n.id] ? 6 : 12) : sh.kind === 'diamond' ? hw * 1.1 : 2 * hw - 8));
          /* state.values { id: text }: a value under the node (valueSide moves it), for a lattice's option values */
          if (view.values && view.values[n.id] != null && view.values[n.id] !== '' && !(dist && dist[n.id] != null)) {
            const vs = n.valueSide || (view.valueSide || {})[n.id] || 'below', vt = String(view.values[n.id]);
            const [vx, vy, va] = vs === 'above' ? [x, y - hh - 12, 'middle'] : vs === 'left' ? [x - hw - 6, y, 'end'] : vs === 'right' ? [x + hw + 6, y, 'start'] : [x, y + hh + 12, 'middle'];
            o.append(vt.includes('$') ? K.lab(vx, vy, vt, { anchor: va, size: 12, halo: true }) : K.txt(vx, vy, vt, { size: 12, weight: 600, halo: true, cls: 'cvb-outink', anchor: va }));
          }
          if (vi >= 0 && view.order !== false) {
            const bx = x + (sh.pill ? hw - 4 : hw * 0.78), by = y - hh * 0.78;
            o.append(svg('circle', { cx: bx, cy: by, r: 9, class: 'cvb-visit' }), K.txt(bx, by + 0.5, String(vi + 1), { cls: 'cvb-visit-t', size: 11 }));
          }
          if (!n.gone) R.tappable(o, n.id, 'Node ' + String(lt).replace(/\n/g, ' '));
          ng.append(o);
        }
        /* item 406: pointers { slow: "n2", fast: "n4" } (or a list [{ id, at, label, side }]): a labelled arrow onto a node,
           above it (side "below" puts it under); several on one node stack; a patch moves them */
        const ptrs = Array.isArray(view.pointers) ? view.pointers : K.isObj(view.pointers) ? Object.entries(view.pointers).map(([id, at]) => (K.isObj(at) ? { id, ...at } : { id, at })) : [];
        const stack = {};
        for (const p of ptrs) {
          const n = byId[p.at]; if (!n || n.gone || p.at == null) continue;
          const [x, y] = pos(n, view), sh = shapeOf(n, view), below = p.side === 'below', key = p.at + (below ? 'b' : 'a'), k = (stack[key] = (stack[key] || 0) + 1) - 1;
          const y0 = below ? y + sh.hh + 3 : y - sh.hh - 3, y1 = below ? y0 + 16 + k * 18 : y0 - 16 - k * 18;
          const o = K.obj(String(p.id), 'cvb-ptr', p.colour || 'manip');
          o.append(K.arrow(x, y1, x, y0, { cls: 'cvb-ln', head: 6 }), K.txt(x, below ? y1 + 9 : y1 - 8, String(p.label ?? p.id), { size: 12, weight: 700, halo: true }));
          lg.append(o);
        }
      },
    };
    return K.make(host, params, ctx, def);
  });
})();
