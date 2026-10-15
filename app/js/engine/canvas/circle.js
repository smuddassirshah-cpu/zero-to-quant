/* circle canvas: the unit circle with an angle, its point, cosine and sine projections, an optional tangent segment,
   arc or sector shading and ticks at the common angles. state.angle is in degrees, or radians when params.degrees is
   false. Drag mode moves the point and emits { id: 'pt', angle, x, y, phase }. Ids: angle, pt, radius, cos, sin, tan,
   arc. Params and state: engine/canvas/README.md. */
(function () {
  'use strict';
  const Z = window.ZQ, C = Z.canvas, { svg, attrs, lerp } = C;

  const RAD = { 0: '0', 30: '\\frac{\\pi}{6}', 45: '\\frac{\\pi}{4}', 60: '\\frac{\\pi}{3}', 90: '\\frac{\\pi}{2}', 120: '\\frac{2\\pi}{3}', 135: '\\frac{3\\pi}{4}', 150: '\\frac{5\\pi}{6}', 180: '\\pi', 210: '\\frac{7\\pi}{6}', 225: '\\frac{5\\pi}{4}', 240: '\\frac{4\\pi}{3}', 270: '\\frac{3\\pi}{2}', 300: '\\frac{5\\pi}{3}', 315: '\\frac{7\\pi}{4}', 330: '\\frac{11\\pi}{6}', 360: '2\\pi' };

  function circle(host, params, ctx = {}) {
    const P = params || {};
    const deg = P.degrees !== false;
    const W = 540, H = 400, cx = 270, cy = 200, R = 138;
    const toDeg = (a) => (deg ? a : a * 180 / Math.PI), fromDeg = (d) => (deg ? d : d * Math.PI / 180);
    const X = (u) => cx + u * R, Y = (v) => cy - v * R;
    const fr = C.frame(host, W, H, { label: P.label || 'Unit circle' });
    const g = fr.g;
    const tickSet = P.ticks === false ? [] : Array.isArray(P.ticks) ? P.ticks.map(t => toDeg(t)) : P.ticks === 'quadrants' ? [0, 90, 180, 270] : [0, 30, 45, 60, 90, 120, 135, 150, 180, 210, 225, 240, 270, 300, 315, 330];
    const angleText = (d) => {
      const r = ((Math.round(d * 1e6) / 1e6) % 360 + 360) % 360;
      if (deg) return { tex: false, s: `${C.fmtNum(d, 1)}°` };
      const k = Math.round(r); if (Math.abs(r - k) < 1e-6 && RAD[k] && Math.abs(d) <= 360) return { tex: true, s: d < 0 ? '-' + RAD[Math.abs(Math.round(d))] : RAD[Math.round(d) === 360 ? 360 : k] };
      return { tex: false, s: C.fmtNum(d * Math.PI / 180, 2) };
    };

    /* Static drawing: axes, circle, ticks */
    const base = svg('g', { class: 'cv-cbase' });
    base.append(
      svg('line', { class: 'cv-axisline', x1: X(-1.22), x2: X(1.22), y1: cy, y2: cy }), svg('line', { class: 'cv-axisline', x1: cx, x2: cx, y1: Y(-1.22), y2: Y(1.22) }),
      svg('path', { class: 'cv-axisend', d: `M${X(1.22) - 6} ${cy - 4}L${X(1.22)} ${cy}L${X(1.22) - 6} ${cy + 4}M${cx - 4} ${Y(1.22) + 6}L${cx} ${Y(1.22)}L${cx + 4} ${Y(1.22) + 6}` }),
      svg('circle', { class: 'cv-unit', cx, cy, r: R }),
      C.label(X(1.22) + 8, cy, 'x', { tex: true, w: 14, h: 20, anchor: 'start' }), C.label(cx + 8, Y(1.22) - 4, 'y', { tex: true, w: 14, h: 20, anchor: 'start' }),
    );
    for (const t of tickSet) {
      const a = t * Math.PI / 180, c = Math.cos(a), s = Math.sin(a);
      base.append(svg('line', { class: 'cv-tick', x1: X(c * 0.95), y1: Y(s * 0.95), x2: X(c * 1.05), y2: Y(s * 1.05) }));
      if (P.tickLabels === false) continue;
      const tx = angleText(t), rr = 1.0 + (tx.tex ? 0.19 : 0.15);
      const lx = X(c * rr), ly = Y(s * rr);
      const onAxis = Math.abs(s) < 1e-9 || Math.abs(c) < 1e-9;
      base.append(C.label(lx + (onAxis && Math.abs(s) < 1e-9 ? 0 : 0), ly + (onAxis && Math.abs(c) < 1e-9 ? 0 : 0), tx.s, { tex: tx.tex, w: 46, h: 34, cls: 'cv-muted cv-ticklabel', size: 12 }));
    }
    g.append(base);

    /* Dynamic parts */
    const mk = (cls, id, kids) => svg('g', { class: 'cv-obj ' + cls, 'data-id': id }, kids);
    const arcShade = mk('cv-arcshade', 'arc', [svg('path', { class: 'cv-body' })]);
    const angleG = mk('cv-anglemark', 'angle', [svg('path', { class: 'cv-body' }), svg('g', { class: 'cv-alab' })]);
    const cosG = mk('cv-seg cv-cos', 'cos', [svg('line', { class: 'cv-body' }), svg('g', { class: 'cv-slab' })]);
    const sinG = mk('cv-seg cv-sin', 'sin', [svg('line', { class: 'cv-body' }), svg('g', { class: 'cv-slab' })]);
    const tanG = mk('cv-seg cv-tan', 'tan', [svg('line', { class: 'cv-ext' }), svg('line', { class: 'cv-body' }), svg('g', { class: 'cv-slab' })]);
    const radG = mk('cv-radius', 'radius', [svg('line', { class: 'cv-body' })]);
    const pt = mk('cv-pt', 'pt', [svg('circle', { class: 'cv-hit', r: 22 }), svg('circle', { class: 'cv-hl-disc', r: 15 }), svg('circle', { class: 'cv-body', r: 6 }), svg('circle', { class: 'cv-knob', r: 9 }), svg('circle', { class: 'cv-knob-ring', r: 10 })]);
    const ptLab = svg('g', { class: 'cv-ptlab' });
    g.append(arcShade, tanG, cosG, sinG, radG, angleG, pt, ptLab);
    const show = { cos: P.showCos !== false, sin: P.showSin !== false, tan: !!P.showTan };
    const lbl = (host2, x, y, tex, anchor = 'middle') => host2.replaceChildren(C.label(x, y, tex, { tex: true, w: 110, h: 30, anchor, cls: 'cv-halo' }));
    const fmtv = (v) => C.fmtNum(Math.abs(v) < 5e-7 ? 0 : v, 2);

    let cur = 0, shadeMode = null;
    const paint = (dAng) => {
      cur = dAng;
      const a = dAng * Math.PI / 180, c = Math.cos(a), s = Math.sin(a);
      const px = X(c), py = Y(s);
      attrs(radG.firstChild, { x1: cx, y1: cy, x2: px, y2: py });
      attrs(pt, { transform: `translate(${px} ${py})` });
      pt.setAttribute('aria-valuenow', C.fmtNum(toDeg2(dAng), 2));
      /* cos along the x-axis, sin from the axis up to the point */
      cosG.style.display = show.cos ? '' : 'none'; sinG.style.display = show.sin ? '' : 'none';
      attrs(cosG.firstChild, { x1: cx, y1: cy, x2: px, y2: cy });
      attrs(sinG.firstChild, { x1: px, y1: cy, x2: px, y2: py });
      const vals = P.values;
      lbl(cosG.lastChild, (cx + px) / 2, cy + (s >= 0 ? 16 : -16), '\\cos\\theta' + (vals ? ' = ' + fmtv(c) : ''));
      lbl(sinG.lastChild, px + (c >= 0 ? 10 : -10), (cy + py) / 2, '\\sin\\theta' + (vals ? ' = ' + fmtv(s) : ''), c >= 0 ? 'start' : 'end');
      cosG.lastChild.style.display = Math.abs(c) < 0.12 ? 'none' : ''; sinG.lastChild.style.display = Math.abs(s) < 0.12 ? 'none' : '';
      /* tangent: the segment of x = 1 from the axis to where the radius line meets it */
      const t = s / c, okT = show.tan && Math.abs(c) > 1e-6 && Math.abs(t) <= 1.35;
      tanG.style.display = okT ? '' : 'none';
      if (okT) {
        attrs(tanG.children[0], { x1: cx, y1: cy, x2: X(1), y2: Y(t) }); attrs(tanG.children[1], { x1: X(1), y1: cy, x2: X(1), y2: Y(t) });
        lbl(tanG.lastChild, X(1) + 8, (cy + Y(t)) / 2, '\\tan\\theta' + (vals ? ' = ' + fmtv(t) : ''), 'start');
      }
      /* angle mark and label */
      const r0 = 30, sweep = ((dAng % 360) + 360) % 360 === 0 && dAng !== 0 ? 359.99 : dAng;
      const big = Math.abs(sweep) > 180 ? 1 : 0, dir = sweep >= 0 ? 0 : 1, ea = sweep * Math.PI / 180;
      attrs(angleG.firstChild, { d: Math.abs(sweep) < 0.5 ? '' : `M${cx + r0} ${cy}A${r0} ${r0} 0 ${big} ${dir} ${cx + r0 * Math.cos(ea)} ${cy - r0 * Math.sin(ea)}` });
      const mid = ea / 2, at = angleText(toDeg2(dAng));
      angleG.lastChild.replaceChildren(Math.abs(sweep) < 8 ? '' : C.label(cx + 50 * Math.cos(mid), cy - 50 * Math.sin(mid), P.angleLabel === 'theta' ? '\\theta' : at.tex ? at.s : at.s.replace('°', '^\\circ'), { tex: true, w: 60, h: 34, cls: 'cv-halo' }));
      /* arc or sector shading from 0 to the angle */
      const sw = Math.max(-359.99, Math.min(359.99, dAng)), e2 = sw * Math.PI / 180, bg = Math.abs(sw) > 180 ? 1 : 0, dr = sw >= 0 ? 0 : 1;
      const end = `${X(Math.cos(e2))} ${Y(Math.sin(e2))}`;
      attrs(arcShade.firstChild, { d: !shadeMode || Math.abs(sw) < 0.5 ? '' : shadeMode === 'sector' ? `M${cx} ${cy}L${X(1)} ${cy}A${R} ${R} 0 ${bg} ${dr} ${end}Z` : `M${X(1)} ${cy}A${R} ${R} 0 ${bg} ${dr} ${end}` });
      arcShade.classList.toggle('is-sector', shadeMode === 'sector');
      /* optional coordinate label at the point */
      ptLab.replaceChildren(P.coords ? C.label(px + (c >= 0 ? 14 : -14), py + (s >= 0 ? -16 : 16), `(${fmtv(c)}, ${fmtv(s)})`, { tex: true, w: 120, h: 26, anchor: c >= 0 ? 'start' : 'end', cls: 'cv-halo' }) : '');
    };
    const toDeg2 = (d) => (deg ? d : d); // display angle stays in degrees internally; angleText converts
    const anim = C.animator();
    const draw = (st, prev, { instant, ms }) => {
      shadeMode = st.shade || null;
      const target = toDeg(st.angle ?? 0);
      if (instant) { anim.stop(); paint(target); return; }
      const from = cur; anim.run(ms, (t) => paint(lerp(from, target, t)));
    };

    /* Drag the point around the circle; snaps to `snap` degrees and is pulled onto common angles within 3° */
    const snapDeg = P.snap ?? 1;
    const setFromXY = (p, phase) => {
      let d = Math.atan2(cy - p.y, p.x - cx) * 180 / Math.PI; if (d < 0) d += 360;
      const near = tickSet.concat(360).find(t => Math.abs(t - d) <= 3); if (near != null) d = near % 360;
      else if (snapDeg) d = Math.round(d / snapDeg) * snapDeg % 360;
      emitAngle(d, phase);
    };
    const emitAngle = (d, phase) => {
      paint(d); const v = fromDeg(d); I.setQuiet({ angle: v });
      I.emit('change', { id: 'pt', angle: v, x: Math.cos(d * Math.PI / 180), y: Math.sin(d * Math.PI / 180), phase });
    };
    C.dragger(pt, fr.svg, { start: () => !(I.locked() || I.mode() !== 'drag'), move: (p) => setFromXY(p, 'move'), end: (p) => setFromXY(p, 'end') });
    pt.addEventListener('keydown', (e) => {
      if (I.mode() !== 'drag' || I.locked()) return;
      const k = { ArrowRight: -1, ArrowDown: -1, ArrowLeft: 1, ArrowUp: 1 }[e.key]; if (!k) return;
      e.preventDefault(); emitAngle(((cur + k * (e.shiftKey ? 15 : Math.max(1, snapDeg))) % 360 + 360) % 360, 'end');
    });
    const I = C.instance({
      kind: 'circle', factory: circle, params, ctx, fr, draw, defaults: { angle: deg ? 30 : Math.PI / 6 },
      onEnable: (mode) => { const on = mode === 'drag'; pt.classList.toggle('cv-handle', on); if (on) { pt.setAttribute('tabindex', '0'); pt.setAttribute('role', 'slider'); pt.setAttribute('aria-label', 'Angle'); } else ['tabindex', 'role', 'aria-label'].forEach(a => pt.removeAttribute(a)); },
    });
    const api = I.api;
    api.points = () => { const a = cur * Math.PI / 180; return { pt: { x: Math.cos(a), y: Math.sin(a), angle: I.state().angle } }; };
    api.place = (id, pos, { instant = false } = {}) => api.set({ angle: typeof pos === 'number' ? pos : fromDeg(((Math.atan2(pos[1], pos[0]) * 180 / Math.PI) + 360) % 360) }, { instant });
    api.param = (name, v) => { if (name === 'angle') api.set({ angle: v }, { instant: true }); };
    if (P.drag) pt.classList.add('cv-handle');
    api.set({}, { instant: true });
    return api;
  }

  C.register('circle', circle);
})();
