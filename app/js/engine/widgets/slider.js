/* slider widget (design-research 5.3 no. 5): 4px track, 24px thumb in the manipulable blue, 44px hit area,
   value label above the thumb, optional snap ticks; arrow keys step and Shift+arrow steps ten times.
   spec: { kind: 'slider', min, max, step, start, bind, label, unitLabel, format, answer, tol, wrong: [{ id, from, to }] }
   format: "fraction" shows the value as a fraction in lowest terms (0.375 reads 3/8), on the thumb and the ends.
   bind drives the canvas live: "p" sets state.params.p; a dotted path such as "strike.c1" sets state.strike.c1.
   Without `answer` it is an explore control (grade() is always ok), which is how canvas.controls entries render. */
(function () {
  'use strict';
  const Z = window.ZQ;

  Z.widgets.register('slider', (host, spec, ctx) => {
    const min = +(spec.min ?? 0), max = +(spec.max ?? 1), step = +(spec.step ?? ((max - min) / 100 || 0.01));
    const dp = (() => { const s = String(+step.toFixed(10)); const i = s.indexOf('.'); return i < 0 ? 0 : s.length - i - 1; })();
    const unit = spec.unitLabel || '';
    const fmt = (v) => {
      if (spec.format === 'fraction') { const f = Z.grade.fmtFrac(+(+v).toFixed(10)).replace('-', '−'); return unit ? `${f} ${unit}` : f; }
      let n = (+v).toFixed(dp); if (/^-0(\.0+)?$/.test(n)) n = n.slice(1);
      n = n.replace('-', '−');
      if (Math.abs(v) >= 1000) n = (v < 0 ? '−' : '') + Math.abs(+v).toLocaleString('en-GB', { minimumFractionDigits: dp, maximumFractionDigits: dp });
      if (!unit) return n;
      if (/^[£$€]$/.test(unit)) return (v < 0 ? '−' : '') + unit + n.replace('−', '');
      return unit === '%' ? n + '%' : n + ' ' + unit;
    };
    const snap = (v) => { const k = Math.round((v - min) / step); return Math.min(max, Math.max(min, +(min + k * step).toFixed(Math.min(10, dp + 2)))); };
    const start = snap(spec.start ?? (min + max) / 2);
    const name = spec.label || spec.bind || 'Value';
    const nTicks = Math.round((max - min) / step);
    const ticks = spec.ticks === false ? '' : nTicks > 0 && nTicks <= 20 ? Array.from({ length: nTicks + 1 }, (_, i) => `<i style="left:${(i / nTicks) * 100}%"></i>`).join('') : '';
    const el = Z.h(`<div class="wd wd-slider">
      <span class="wd-sl-label">${Z.md(Z.esc(name))}</span>
      <div class="wd-sl-track">
        <span class="wd-sl-val" aria-hidden="true"></span>
        <input type="range" class="slider" min="${min}" max="${max}" step="${step}" value="${start}" aria-label="${Z.esc(String(name).replace(/\$/g, ''))}">
        <div class="wd-sl-ticks" aria-hidden="true">${ticks}</div>
      </div>
      <div class="wd-sl-ends" aria-hidden="true"><span>${fmt(min)}</span><span>${fmt(max)}</span></div>
    </div>`);
    host.append(el);
    const input = el.querySelector('input'), val = el.querySelector('.wd-sl-val');
    let value = start, touched = false;

    const drive = (v, instant = true) => {
      const c = ctx.canvas; if (!c || !spec.bind) return;
      const parts = String(spec.bind).split('.');
      const patch = parts.length === 1 ? { params: { [parts[0]]: v } } : parts.reduceRight((acc, k) => ({ [k]: acc }), v);
      c.set(patch, { instant });
    };
    const show = (v) => {
      const f = (v - min) / ((max - min) || 1);
      val.textContent = fmt(v); val.style.left = `calc(12px + (100% - 24px) * ${f})`;
      input.setAttribute('aria-valuetext', fmt(v));
    };
    const update = (v, { emit = true } = {}) => {
      value = snap(v); input.value = value; show(value); drive(value);
      if (emit) { touched = true; ctx.change({ value }); }
    };
    input.addEventListener('input', () => update(+input.value));
    input.addEventListener('keydown', (e) => {
      if (!e.shiftKey) return;
      const dir = { ArrowRight: 1, ArrowUp: 1, ArrowLeft: -1, ArrowDown: -1 }[e.key]; if (!dir) return;
      e.preventDefault(); update(value + dir * step * 10);
    });
    show(start);
    /* Apply the start value so the canvas and control agree from the first frame. */
    if (spec.bind && ctx.canvas) drive(start);

    const clearMarks = () => el.classList.remove('is-correct', 'is-notyet', 'is-reveal');
    return {
      el,
      value: () => value,
      set(v) { if (v == null || !Number.isFinite(+v)) return; update(+v, { emit: false }); },
      grade() {
        if (spec.answer == null) return { ok: true, key: null, detail: { value } };
        const ok = Math.abs(value - spec.answer) <= (+spec.tol || 0) + 1e-9;
        let key = null;
        if (!ok) for (const w of spec.wrong || []) { if (value >= w.from - 1e-9 && value <= w.to + 1e-9) { key = w.id; break; } }
        return { ok, key, detail: { value, touched } };
      },
      lock() { input.disabled = true; },
      unlock() { input.disabled = false; clearMarks(); },
      markGraded(res) { clearMarks(); if (res) el.classList.add(res.ok ? 'is-correct' : 'is-notyet'); },
      reveal() {
        if (spec.answer == null) return Promise.resolve();
        clearMarks(); el.classList.add('is-reveal');
        const from = value, to = snap(spec.answer);
        return Z.canvas.tween(from, to, 600, (v) => { value = v; input.value = v; show(v); drive(v); }).then(() => { value = to; input.value = to; show(to); drive(to); });
      },
      reset() { clearMarks(); touched = false; input.disabled = false; update(start, { emit: false }); },
      focus() { input.focus(); },
      destroy() { el.remove(); },
    };
  });
})();
