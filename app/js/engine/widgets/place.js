/* Place widget: tokens into slots (docs/AUTHORING.md 3, design-research 5.3 no. 7).
   mode "assign": each slot accepts the tokens listed in its accepts[]; tokens accepted nowhere belong in the bank.
   mode "order": one slot, graded on the token sequence against order[].
   Pointer: drag a lipped token onto a slot or back to the bank, or tap a token then tap where it goes.
   Keyboard: Space lifts the focused token, arrows choose the target (bank or a slot), Space drops, Escape cancels.
   Key on a wrong answer: the first misplaced token. */
(function () {
  'use strict';
  const Z = window.ZQ;

  Z.widgets.register('place', (host, spec, ctx) => {
    const tokens = spec.tokens || [];
    const mode = spec.mode === 'order' ? 'order' : 'assign';
    const slots = mode === 'order' ? (spec.slots && spec.slots.length ? spec.slots.slice(0, 1) : [{ id: 'seq', label: '' }]) : (spec.slots || []);
    const tokById = Object.fromEntries(tokens.map(t => [t.id, t]));
    const bankStart = spec.shuffle === false ? tokens.map(t => t.id) : Z.widgets.shuffle(tokens.map(t => t.id), ctx.rng || Math.random);
    const el = Z.h(`<div class="wd-place wd-place-${mode}">
      <div class="wd-slots">${slots.map(s => `
        <div class="wd-slotrow">${s.label ? `<span class="t-label wd-slot-l">${Z.grade.inline(s.label)}</span>` : ''}
          <div class="wd-slot" data-slot="${Z.esc(s.id)}" role="group" aria-label="${Z.esc(s.label ? 'Slot: ' + s.label.replace(/\$/g, '') : 'Answer slot')}"><span class="wd-slot-ph t-caption">${mode === 'order' ? 'Place the tokens here in order' : 'Drop here'}</span></div>
        </div>`).join('')}</div>
      <div class="wd-bank" data-slot="bank" role="group" aria-label="Tokens to place"></div>
      <p class="t-caption wd-order-help">Drag a token into place, or tap it and then tap a slot. Keyboard: Space, arrows, Space.</p>
      <p class="sr-only" aria-live="assertive"></p>
    </div>`);
    host.append(el);
    const live = el.querySelector('[aria-live]');
    const bank = el.querySelector('.wd-bank');
    const zones = () => [bank, ...el.querySelectorAll('.wd-slot')];
    const zoneOf = (id) => (id === 'bank' ? bank : el.querySelector(`.wd-slot[data-slot="${CSS.escape(id)}"]`));
    const tokEl = (id) => el.querySelector(`.wd-tok[data-id="${CSS.escape(id)}"]`);
    const mk = (id) => Z.h(`<button type="button" class="wd-tok wd-chip" data-id="${Z.esc(id)}">${Z.grade.inline(tokById[id]?.text ?? id)}<span class="wd-tok-mark" aria-hidden="true"></span></button>`);
    bankStart.forEach(id => bank.append(mk(id)));
    let locked = false, sel = null, target = -1;
    const say = (t) => { live.textContent = t; };
    const syncPh = () => el.querySelectorAll('.wd-slot').forEach(s => { s.querySelector('.wd-slot-ph').hidden = !!s.querySelector('.wd-tok'); });
    const value = () => {
      if (mode === 'order') return [...zoneOf(slots[0].id).querySelectorAll('.wd-tok')].map(n => n.dataset.id);
      return Object.fromEntries(slots.map(s => [s.id, [...zoneOf(s.id).querySelectorAll('.wd-tok')].map(n => n.dataset.id)]));
    };
    const changed = () => { syncPh(); ctx.change && ctx.change(value()); };
    const animateMove = (n, mutate) => {
      const a = n.getBoundingClientRect();
      mutate();
      if (Z.reducedMotion()) return;
      const b = n.getBoundingClientRect();
      n.animate([{ transform: `translate(${a.left - b.left}px, ${a.top - b.top}px)` }, { transform: 'none' }], { duration: 300, easing: getComputedStyle(document.documentElement).getPropertyValue('--spring-snap').trim() || 'ease-out' });
    };
    const put = (id, zoneId, before = null) => {
      const n = tokEl(id), z = zoneOf(zoneId); if (!n || !z) return;
      animateMove(n, () => { if (before && before.parentElement === z) z.insertBefore(n, before); else z.append(n); });
      Z.sound('tap'); changed();
    };
    const select = (n) => {
      el.querySelectorAll('.wd-tok.is-lifted').forEach(x => x.classList.remove('is-lifted'));
      sel = n; if (n) n.classList.add('is-lifted');
      el.classList.toggle('has-sel', !!n);
    };
    const setTarget = (i) => { const zs = zones(); zs.forEach((z, k) => z.classList.toggle('is-target', k === i)); target = i; if (zs[i]) say(zs[i] === bank ? 'Target: the token bank.' : `Target: ${zs[i].getAttribute('aria-label')}.`); };

    el.addEventListener('click', (e) => {
      if (locked || el.dataset.dragged) { delete el.dataset.dragged; return; }
      const t = e.target.closest('.wd-tok');
      const z = e.target.closest('.wd-slot, .wd-bank');
      if (t && (!sel || sel === t)) { select(sel === t ? null : t); return; }
      if (sel && z) {
        const before = t && t.parentElement === z ? t : null;
        put(sel.dataset.id, z.dataset.slot, before); select(null); return;
      }
      if (t) select(t);
    });
    el.addEventListener('keydown', (e) => {
      if (locked) return;
      const t = e.target.closest('.wd-tok');
      if (e.key === ' ' && t) {
        e.preventDefault();
        if (sel === t && target >= 0) { const z = zones()[target]; put(t.dataset.id, z.dataset.slot); select(null); setTarget(-1); t.focus(); say('Dropped.'); }
        else { select(t); setTarget(zones().indexOf(t.parentElement)); say('Lifted. Use the arrow keys to choose a slot, then Space.'); }
        return;
      }
      if (e.key === 'Escape' && sel) { e.preventDefault(); e.stopPropagation(); select(null); setTarget(-1); return; }
      const d = { ArrowDown: 1, ArrowRight: 1, ArrowUp: -1, ArrowLeft: -1 }[e.key];
      if (d && sel && t === sel) { e.preventDefault(); const n = zones().length; setTarget(((target < 0 ? 0 : target) + d + n) % n); }
    });

    /* Pointer drag with a floating clone */
    let drag = null;
    el.addEventListener('pointerdown', (e) => {
      const t = e.target.closest('.wd-tok'); if (!t || locked || e.button !== 0) return;
      drag = { t, x0: e.clientX, y0: e.clientY, on: false, id: e.pointerId };
      t.setPointerCapture(e.pointerId);
    });
    el.addEventListener('pointermove', (e) => {
      if (!drag || drag.id !== e.pointerId) return;
      const dx = e.clientX - drag.x0, dy = e.clientY - drag.y0;
      if (!drag.on) { if (Math.hypot(dx, dy) < 5) return; drag.on = true; drag.t.classList.add('is-lifted', 'is-dragging'); }
      drag.t.style.transform = `translate(${dx}px, ${dy}px) scale(1.03)`;
      drag.t.style.pointerEvents = 'none';
      const under = document.elementFromPoint(e.clientX, e.clientY);
      const z = under && under.closest('.wd-slot, .wd-bank');
      zones().forEach(x => x.classList.toggle('is-target', x === z));
      drag.over = z; drag.before = under && under.closest('.wd-tok');
    });
    const end = (e) => {
      if (!drag || drag.id !== e.pointerId) return;
      const d = drag; drag = null;
      if (!d.on) return;
      el.dataset.dragged = '1'; setTimeout(() => { delete el.dataset.dragged; }, 0);
      d.t.classList.remove('is-dragging', 'is-lifted'); d.t.style.pointerEvents = '';
      const r0 = d.t.getBoundingClientRect();
      d.t.style.transform = '';
      zones().forEach(x => x.classList.remove('is-target'));
      if (d.over) {
        const before = d.before && d.before.parentElement === d.over && d.before !== d.t ? d.before : null;
        const r1 = d.t.getBoundingClientRect();
        if (before) d.over.insertBefore(d.t, before); else d.over.append(d.t);
        const r2 = d.t.getBoundingClientRect();
        if (!Z.reducedMotion()) d.t.animate([{ transform: `translate(${r0.left - r2.left}px, ${r0.top - r2.top}px)` }, { transform: 'none' }], { duration: 300, easing: getComputedStyle(document.documentElement).getPropertyValue('--spring-snap').trim() || 'ease-out' });
        void r1; Z.sound('tap'); changed();
      } else if (!Z.reducedMotion()) {
        const r2 = d.t.getBoundingClientRect();
        d.t.animate([{ transform: `translate(${r0.left - r2.left}px, ${r0.top - r2.top}px)` }, { transform: 'none' }], { duration: 300, easing: 'cubic-bezier(0.2, 0, 0, 1)' });
      }
      select(null);
    };
    el.addEventListener('pointerup', end); el.addEventListener('pointercancel', end);

    const strip = () => el.querySelectorAll('.wd-tok').forEach(n => { n.classList.remove('ok', 'bad', 'wd-rev', 'dim'); n.querySelector('.wd-tok-mark').innerHTML = ''; });
    const home = Object.fromEntries(tokens.map(t => [t.id, 'bank']));
    if (mode === 'assign') slots.forEach(s => (s.accepts || []).forEach(id => { home[id] = s.id; }));
    const misplaced = () => {
      const v = value();
      if (mode === 'order') {
        const want = spec.order || [];
        const i = v.findIndex((id, k) => id !== want[k]);
        if (i >= 0) return v[i];
        if (v.length < want.length) return want[v.length];
        return null;
      }
      const where = {}; tokens.forEach(t => { where[t.id] = 'bank'; });
      Object.entries(v).forEach(([s, list]) => list.forEach(id => { where[id] = s; }));
      // order of checking: tokens in the order they appear on screen
      const seen = [...el.querySelectorAll('.wd-tok')].map(n => n.dataset.id);
      return seen.find(id => where[id] !== home[id]) || null;
    };
    const setValue = (v) => {
      [...el.querySelectorAll('.wd-tok')].forEach(n => bank.append(n));
      if (mode === 'order') (v || []).forEach(id => { const n = tokEl(id); if (n) zoneOf(slots[0].id).append(n); });
      else Object.entries(v || {}).forEach(([s, list]) => (list || []).forEach(id => { const n = tokEl(id), z = zoneOf(s); if (n && z) z.append(n); }));
      changed();
    };
    const correct = () => (mode === 'order' ? (spec.order || []).slice() : Object.fromEntries(slots.map(s => [s.id, (s.accepts || []).slice()])));
    return {
      el,
      value,
      set: setValue,
      answer: correct,
      ready: () => (mode === 'order' ? value().length > 0 : Object.values(value()).some(l => l.length)),
      grade() {
        const k = misplaced();
        return { ok: !k, key: k, detail: { value: value() } };
      },
      lock() { locked = true; select(null); setTarget(-1); el.classList.add('is-locked'); el.querySelectorAll('.wd-tok').forEach(n => n.setAttribute('aria-disabled', 'true')); },
      unlock() { locked = false; strip(); el.classList.remove('is-locked'); el.querySelectorAll('.wd-tok').forEach(n => n.setAttribute('aria-disabled', 'false')); },
      markGraded(res) {
        strip();
        const v = value();
        const where = {};
        if (mode === 'order') v.forEach((id, i) => { where[id] = (spec.order || [])[i] === id; });
        else Object.entries(v).forEach(([s, list]) => list.forEach(id => { where[id] = home[id] === s; }));
        Object.entries(where).forEach(([id, ok]) => { const n = tokEl(id); n.classList.add(res.ok || ok ? 'ok' : 'bad'); n.querySelector('.wd-tok-mark').innerHTML = Z.icon(res.ok || ok ? 'check' : 'cross'); });
      },
      reveal() { setValue(correct()); strip(); locked = true; el.classList.add('is-locked'); el.querySelectorAll('.wd-slot .wd-tok').forEach(n => n.classList.add('wd-rev')); el.querySelectorAll('.wd-bank .wd-tok').forEach(n => n.classList.add('dim')); },
      reset() { strip(); locked = false; el.classList.remove('is-locked'); setValue(mode === 'order' ? [] : {}); },
      focus() { el.querySelector('.wd-tok')?.focus({ preventScroll: true }); },
      destroy() { drag = null; },
    };
  });
})();
