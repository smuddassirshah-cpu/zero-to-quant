/* boxes canvas: containers (urn, bag, box, hand, row of slots) holding items (ball, card, coin, slot) for counting and
   drawing without replacement. state.draw moves items to the hand, state.move to any container, state.face turns cards
   and coins (a coin shows H or T unless it has a label). Item kinds: ball, card, coin, slot, and bag (alias sealed: a
   closed sack showing only its label, for "a bag of n counters"). Drag mode lets the learner place items in
   containers and emits { id, container }. Ids: item ids, container
   ids, and row slots <container>-<k> (one-based). Params and state: engine/canvas/README.md. */
(function () {
  'use strict';
  const Z = window.ZQ, C = Z.canvas, { svg, attrs, lerp } = C;

  const SIZE = { ball: [26, 26], coin: [28, 28], card: [26, 36], slot: [28, 36], bag: [32, 34] };
  const KIND = (k) => (k === 'sealed' ? 'bag' : k); // "sealed" is an alias of "bag": a closed bag whose contents are hidden

  function boxes(host, params, ctx = {}) {
    const P = params || {};
    const conts = (P.containers || []).map(c => ({ kind: 'box', ...c, items: c.items || [] }));
    const items = new Map();
    conts.forEach(c => c.items.forEach(it => { const v = { kind: P.itemKind || 'ball', ...it, home: c.id }; v.kind = KIND(v.kind); items.set(it.id, v); }));
    const total = items.size;
    /* items 102 and 111: a card is as wide as its label (a file name fits on one card); a wide card is a little shorter */
    const sizeOf = (it) => {
      if (it.kind !== 'card') return SIZE[it.kind] || SIZE.ball;
      const w = Math.ceil(C.textW(String(it.label ?? ''), 13, 600)) + 14;
      return w > SIZE.card[0] ? [Math.min(200, w), 30] : SIZE.card;
    };
    const maxSz = [...items.values()].reduce((m, it) => { const z = sizeOf(it); return [Math.max(m[0], z[0]), Math.max(m[1], z[1])]; }, [0, 0]);
    const hand = conts.find(c => c.kind === 'hand') || null;

    /* ---- Layout: containers side by side, bottoms aligned, labels below ---- */
    let pitchX = maxSz[0] + 8, pitchY = maxSz[1] + 6;
    const capOf = (c) => c.capacity || (c.kind === 'row' ? (c.slots || c.items.length || 3) : c.kind === 'hand' ? Math.max(c.items.length, Math.min(total, 10), 3) : Math.max(c.items.length, 1));
    const geom = (c, px, py) => {
      const cap = capOf(c), lineish = c.kind === 'hand' || c.kind === 'row';
      const cols = c.cols || (lineish ? Math.min(cap, 10) : Math.min(6, Math.max(2, Math.ceil(Math.sqrt(cap * 1.4)))));
      const rows = Math.max(1, Math.ceil(cap / cols));
      const iw = cols * px, ih = rows * py;
      const pad = { urn: [18, 46, 10], bag: [22, 38, 12], box: [12, 10, 8], hand: [10, 10, 10], row: [4, 4, 4] }[c.kind] || [12, 10, 8];
      return { cap, cols, rows, iw, ih, w: iw + 2 * pad[0], h: ih + pad[1] + pad[2], padX: pad[0], padTop: pad[1] };
    };
    let G = conts.map(c => geom(c, pitchX, pitchY));
    const gapX = 34;
    let need = G.reduce((s, g) => s + g.w, 0) + gapX * (conts.length - 1) + 24;
    if (need > 540) { const k = Math.max(0.6, (540 - 24 - gapX * (conts.length - 1)) / (need - 24 - gapX * (conts.length - 1))); pitchX *= k; pitchY *= k; G = conts.map(c => geom(c, pitchX, pitchY)); need = G.reduce((s, g) => s + g.w, 0) + gapX * (conts.length - 1) + 24; }
    const scaleItem = Math.min(1, pitchX / (maxSz[0] + 8));
    const lift = hand ? 0 : 50;
    const maxH = Math.max(...G.map(g => g.h), 40);
    const W = 540, baseY = 12 + lift + maxH, H = baseY + 34;
    let x = (W - need) / 2 + 12;
    const box = new Map();
    conts.forEach((c, i) => { const g = G[i]; box.set(c.id, { c, g, x, y: baseY - g.h }); x += g.w + gapX; });

    const slotPos = (cid, k) => {
      const b = box.get(cid), g = b.g, lineish = b.c.kind === 'hand' || b.c.kind === 'row';
      const col = k % g.cols, row = Math.floor(k / g.cols);
      const ix = b.x + g.padX + (col + 0.5) * pitchX;
      const fromTop = b.c.fill === 'top' || (lineish && b.c.fill !== 'bottom'); // fill: "top" | "bottom" (default: top for hand and row, bottom for the rest)
      const iy = fromTop ? b.y + g.padTop + (row + 0.5) * pitchY : b.y + g.padTop + g.ih - (row + 0.5) * pitchY;
      return { x: ix, y: iy };
    };

    const fr = C.frame(host, W, H, { label: P.label || 'Containers and items' });
    const g = fr.g;
    const contG = svg('g', { class: 'cv-conts' }), itemG = svg('g', { class: 'cv-items' });
    g.append(contG, itemG);
    const shapePath = (c, x0, y0, w, h) => {
      if (c.kind === 'urn') { const a = x0 + w * 0.3, b = x0 + w * 0.7; return `M${a} ${y0}L${a} ${y0 + 10}C${a} ${y0 + 24} ${x0} ${y0 + 20} ${x0} ${y0 + 40}L${x0} ${y0 + h - 16}Q${x0} ${y0 + h} ${x0 + 16} ${y0 + h}L${x0 + w - 16} ${y0 + h}Q${x0 + w} ${y0 + h} ${x0 + w} ${y0 + h - 16}L${x0 + w} ${y0 + 40}C${x0 + w} ${y0 + 20} ${b} ${y0 + 24} ${b} ${y0 + 10}L${b} ${y0}`; }
      if (c.kind === 'bag') { const a = x0 + w * 0.38, b = x0 + w * 0.62, r = 20; return `M${a} ${y0 + 14}C${x0 + w * 0.1} ${y0 + 22} ${x0} ${y0 + h * 0.4} ${x0} ${y0 + h - r}Q${x0} ${y0 + h} ${x0 + r} ${y0 + h}L${x0 + w - r} ${y0 + h}Q${x0 + w} ${y0 + h} ${x0 + w} ${y0 + h - r}C${x0 + w} ${y0 + h * 0.4} ${x0 + w * 0.9} ${y0 + 22} ${b} ${y0 + 14}Z`; }
      if (c.kind === 'box') return `M${x0 + 6} ${y0}Q${x0} ${y0} ${x0} ${y0 + 6}L${x0} ${y0 + h - 6}Q${x0} ${y0 + h} ${x0 + 6} ${y0 + h}L${x0 + w - 6} ${y0 + h}Q${x0 + w} ${y0 + h} ${x0 + w} ${y0 + h - 6}L${x0 + w} ${y0 + 6}Q${x0 + w} ${y0} ${x0 + w - 6} ${y0}Z`; // closed on all four sides (item 92)
      return '';
    };
    for (const b of box.values()) {
      const { c, g: gg } = b;
      const grp = svg('g', { class: 'cv-obj cv-cont cv-cont-' + c.kind, 'data-id': c.id });
      if (c.kind === 'hand') grp.append(svg('rect', { class: 'cv-body cv-tray', x: b.x, y: b.y, width: gg.w, height: gg.h, rx: 12 }));
      else if (c.kind === 'row') for (let k = 0; k < gg.cap; k++) { const p = slotPos(c.id, k); grp.append(svg('g', { class: 'cv-obj cv-slot', 'data-id': `${c.id}-${k + 1}` }, [svg('rect', { class: 'cv-body', x: p.x - pitchX / 2 + 2, y: p.y - pitchY / 2 + 1, width: pitchX - 4, height: pitchY - 2, rx: 5 })])); }
      else grp.append(svg('path', { class: 'cv-body', d: shapePath(c, b.x, b.y, gg.w, gg.h) }));
      if (c.kind === 'urn') grp.append(svg('path', { class: 'cv-rim', d: `M${b.x + gg.w * 0.25} ${b.y}H${b.x + gg.w * 0.75}` }));
      if (c.kind === 'bag') grp.append(svg('path', { class: 'cv-rim', d: `M${b.x + gg.w * 0.36} ${b.y + 6}Q${b.x + gg.w / 2} ${b.y + 20} ${b.x + gg.w * 0.64} ${b.y + 6}` }));
      if (c.label) grp.append(C.label(b.x + gg.w / 2, baseY + 18, c.label, { cls: 'cv-muted', tex: 'auto' }));
      contG.append(grp); b.el = grp;
    }

    /* ---- Items ---- */
    const el = new Map();
    for (const it of items.values()) {
      const [w, h] = sizeOf(it).map(v => v * scaleItem);
      const colour = it.colour == null ? (it.kind === 'ball' ? 1 : it.kind === 'coin' ? 4 : 0) : it.colour;
      const grp = svg('g', { class: `cv-obj cv-item cv-${it.kind}${colour ? ' cv-k' + colour : ' cv-plain'}`, 'data-id': it.id, 'data-tap': '', 'data-label': `${it.label || it.kind} ${it.id}` });
      const flip = svg('g', { class: 'cv-flip' });
      if (it.kind === 'card') {
        flip.append(svg('rect', { class: 'cv-body', x: -w / 2, y: -h / 2, width: w, height: h, rx: 4 }), svg('g', { class: 'cv-back' }, [svg('rect', { x: -w / 2 + 3, y: -h / 2 + 3, width: w - 6, height: h - 6, rx: 2 })]), C.label(0, 0.5, it.label ?? '', { cls: 'cv-itext', size: 13 }));
      } else if (it.kind === 'bag') {
        /* a sealed bag: a tied sack, its label (often "?" or "n") on the front */
        flip.append(svg('path', { class: 'cv-body', d: `M${-w * 0.16} ${-h / 2 + 6}C${-w / 2} ${-h * 0.2} ${-w / 2} ${h / 2} ${-w * 0.3} ${h / 2}H${w * 0.3}C${w / 2} ${h / 2} ${w / 2} ${-h * 0.2} ${w * 0.16} ${-h / 2 + 6}Z` }),
          svg('path', { class: 'cv-bagtie', d: `M${-w * 0.2} ${-h / 2 + 2}L${w * 0.2} ${-h / 2 + 8}M${w * 0.2} ${-h / 2 + 2}L${-w * 0.2} ${-h / 2 + 8}` }),
          C.label(0, h * 0.12, it.label ?? '', { cls: 'cv-itext', size: 12, tex: 'auto', w: w, h: 20 }));
      } else if (it.kind === 'slot') {
        flip.append(svg('rect', { class: 'cv-body', x: -w / 2, y: -h / 2, width: w, height: h, rx: 5 }), C.label(0, 0.5, it.label ?? '', { cls: 'cv-itext' }));
      } else {
        flip.append(svg('circle', { class: 'cv-body', r: w / 2 }), C.label(0, 0.5, it.label ?? '', { cls: 'cv-itext', size: it.kind === 'coin' ? 13 : 12 }));
      }
      grp.append(svg('circle', { class: 'cv-hit', r: Math.max(w, h) / 2 + 6 }), flip);
      itemG.append(grp);
      el.set(it.id, { grp, flip, text: flip.querySelector('.cv-itext'), it, pos: null, face: null, scale: 1 });
      C.dragger(grp, fr.svg, {
        start: () => !(I.locked() || I.mode() !== 'drag' || (I.modeOpts().ids && !I.modeOpts().ids.includes(it.id))),
        move: (p0) => { const p = { x: p0.x, y: p0.y + off }; const e = el.get(it.id); e.pos = { x: p.x, y: p.y }; paintItem(e); grp.classList.add('is-lifted'); I.emit('change', { id: it.id, x: p.x, y: p.y, phase: 'move' }); },
        end: (p0) => { grp.classList.remove('is-lifted'); drop(it.id, { x: p0.x, y: p0.y + off }); },
      });
      grp.addEventListener('keydown', (ev) => {
        if (I.mode() !== 'drag' || I.locked()) return;
        const k = { ArrowRight: 1, ArrowLeft: -1 }[ev.key]; if (!k) return;
        ev.preventDefault();
        const cur = where(I.state()).get(it.id), i = conts.findIndex(c => c.id === cur), next = conts[(i + k + conts.length) % conts.length];
        placeIn(it.id, next.id);
      });
    }

    /* Where every item is for a state: home, then draw (to the hand), then move */
    const where = (st) => {
      const loc = new Map([...items.values()].map(i => [i.id, i.home]));
      (st.draw || []).forEach(id => { if (items.has(id)) loc.set(id, hand ? hand.id : '@drawn'); });
      Object.entries(st.move || {}).forEach(([id, c]) => { if (items.has(id) && (box.has(c) || c === '@drawn')) loc.set(id, c); });
      return loc;
    };
    const order = (st) => {
      const seq = [...items.keys()], arrivals = [...(st.draw || []), ...Object.keys(st.move || {})];
      return [...seq.filter(id => !arrivals.includes(id)), ...arrivals.filter((id, i) => arrivals.lastIndexOf(id) === i && items.has(id))];
    };
    const targets = (st) => {
      const loc = where(st), count = new Map(), out = new Map();
      let drawnK = 0; const drawnN = [...loc.values()].filter(v => v === '@drawn').length;
      for (const id of order(st)) {
        const c = loc.get(id);
        if (c === '@drawn') { out.set(id, { x: W / 2 + (drawnK++ - (drawnN - 1) / 2) * (pitchX + 6), y: 12 + lift / 2 - 4 }); continue; }
        const k = count.get(c) || 0; count.set(c, k + 1);
        out.set(id, slotPos(c, k));
      }
      return out;
    };
    const faceOf = (st, it) => { const f = (st.face || {})[it.id] ?? it.face; if (it.kind === 'coin') return f === 'down' || f === 'T' ? 'T' : 'H'; return f === 'down' ? 'down' : 'up'; };
    const paintItem = (e) => { if (e.pos) attrs(e.grp, { transform: `translate(${e.pos.x} ${e.pos.y})` }); attrs(e.flip, { transform: `scale(${e.scale} 1)` }); };
    const paintFace = (e, f) => {
      e.grp.classList.toggle('is-down', f === 'down');
      if (e.it.kind === 'coin' && e.text && e.it.label == null) e.text.textContent = f; // a coin shows its face, H or T, unless it has a label
    };

    const anim = C.animator();
    /* Without a hand container the band above the containers (where drawn items wait) shows only while an item is
       drawn; otherwise the drawing moves up and loses it */
    let off = -1;
    const band = (st) => {
      const want = hand || [...where(st).values()].includes('@drawn') ? 0 : lift;
      if (want === off) return;
      off = want; g.setAttribute('transform', `translate(0 ${-off})`); fr.resize(W, H - off);
    };
    const draw = (st, prev, { instant, ms }) => {
      band(st);
      const T = targets(st);
      const moves = [];
      for (const [id, e] of el) {
        const to = T.get(id), from = e.pos || to, f = faceOf(st, e.it), flipping = e.face != null && e.face !== f;
        moves.push({ e, from, to, f, flipping, travel: Math.hypot(to.x - from.x, to.y - from.y) > 1 });
      }
      const frame = (t) => {
        for (const m of moves) {
          const arc = m.travel ? Math.sin(Math.PI * t) * Math.min(46, 16 + Math.hypot(m.to.x - m.from.x, m.to.y - m.from.y) * 0.18) : 0;
          m.e.pos = { x: lerp(m.from.x, m.to.x, t), y: lerp(m.from.y, m.to.y, t) - arc };
          if (m.flipping) { m.e.scale = Math.abs(1 - 2 * t) || 0.001; paintFace(m.e, t < 0.5 ? m.e.face : m.f); } else paintFace(m.e, m.f);
          if (t === 1) { m.e.face = m.f; m.e.scale = 1; }
          paintItem(m.e);
        }
      };
      if (instant) { anim.stop(); frame(1); } else anim.run(ms, frame);
    };
    /* Drag drop: the container under the pointer takes the item; outside every container it returns */
    const drop = (id, p) => {
      let hit = null;
      for (const b of box.values()) if (p.x >= b.x - 10 && p.x <= b.x + b.g.w + 10 && p.y >= b.y - 30 && p.y <= baseY + 24) hit = b.c.id;
      if (hit && hit !== where(I.state()).get(id)) placeIn(id, hit);
      else { I.api.set({}, {}); I.emit('change', { id, container: where(I.state()).get(id), phase: 'end' }); }
    };
    const placeIn = (id, cid) => {
      const st = I.state(), mv = { ...(st.move || {}) }; delete mv[id]; mv[id] = cid;
      I.setQuiet({ move: null }); // replace, not merge, so the key order records arrival order
      I.api.set({ move: mv });
      if (Z.haptic) Z.haptic(10);
      I.emit('change', { id, container: cid, phase: 'end' });
    };

    const I = C.instance({
      kind: 'boxes', factory: boxes, params, ctx, fr, draw,
      onEnable: (mode, opts) => { for (const [id, e] of el) { const on = mode === 'drag' && (!opts.ids || opts.ids.includes(id)); e.grp.classList.toggle('cv-handle', on); if (on) { e.grp.setAttribute('tabindex', '0'); e.grp.setAttribute('role', 'button'); e.grp.setAttribute('aria-label', e.grp.dataset.label + '. Arrow keys move it to another container.'); } else if (mode !== 'tap') ['tabindex', 'role', 'aria-label'].forEach(a => e.grp.removeAttribute(a)); } },
    });
    const api = I.api;
    api.contents = () => { const loc = where(I.state()), out = {}; for (const id of order(I.state())) (out[loc.get(id)] = out[loc.get(id)] || []).push(id); return out; };
    api.points = () => Object.fromEntries([...el].map(([id, e]) => [id, { ...e.pos, container: where(I.state()).get(id) }]));
    api.place = (id, pos, o) => placeIn(id, typeof pos === 'string' ? pos : pos.container);
    api.set({}, { instant: true });
    return api;
  }

  C.register('boxes', boxes);
})();
