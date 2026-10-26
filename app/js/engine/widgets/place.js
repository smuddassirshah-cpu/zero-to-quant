/* Place widget: tokens into slots (docs/AUTHORING.md 3, design-research 5.3 no. 7).
   mode "assign": each slot accepts the tokens listed in its accepts[]; tokens accepted nowhere belong in the bank.
   mode "order": one slot, graded on the token sequence against order[].
   Pointer: drag a lipped token onto a slot or back to the bank, or tap a token then tap where it goes.
   Keyboard: Space lifts the focused token, arrows choose the target (bank or a slot), Space drops, Escape cancels.
   Key on a wrong answer: the first misplaced token.
   Interchangeable tokens: `byText: true` treats tokens with the same text as the same token, and `same: [["t1", "t2"]]`
   (or one list) names groups that are; either slot or position then accepts any member of the group.
   mode "boxes": no tokens or slots of its own; the learner drags the items of the screen's `boxes` canvas into its
   containers. `answer: { "<container>": [itemIds] }` lists what each named container must hold (in any order; with
   `ordered: true` in that order); key = the first item out of place. Items left out of `answer` may be anywhere.
   `count: { "<container>": n }` asks only for how many items a container holds (key "count-<container>"), and
   `free: true` accepts any arrangement once the learner has moved an item (an explore task). */
(function () {
  'use strict';
  const Z = window.ZQ;

  /* mode "boxes": place the items of a boxes canvas into its containers */
  const boxesMode = (host, spec, ctx) => {
    const cv = ctx.canvas;
    const el = Z.h('<div class="wd-drag"><p class="t-caption wd-drag-msg" hidden></p></div>');
    host.append(el);
    const msg = el.querySelector('.wd-drag-msg');
    if (!cv || typeof cv.contents !== 'function') { msg.hidden = false; msg.textContent = 'This task needs its boxes diagram, which could not be drawn.'; return { el, value: () => ({}), grade: () => ({ ok: false, key: null, detail: null }) }; }
    const want = spec.answer || {};
    const ids = spec.items || null;
    cv.enable('drag', ids ? { ids } : {});
    const start = cv.contents();
    let moved = false;
    cv.on('change', (e) => { if (e && e.phase === 'end') { moved = true; ctx.change && ctx.change({ id: e.id, container: e.container }); } });
    const contents = () => cv.contents();
    const where = () => { const w = {}; Object.entries(contents()).forEach(([c, list]) => list.forEach(id => { w[id] = c; })); return w; };
    const misplaced = () => {
      const c = contents(), w = where();
      if (spec.free) return null;
      for (const [cid, n] of Object.entries(spec.count || {})) if ((c[cid] || []).length !== +n) return 'count-' + cid;
      for (const [cid, list] of Object.entries(want)) {
        const have = c[cid] || [];
        const extra = have.find(id => !list.includes(id)); if (extra) return extra;
        const miss = list.find(id => w[id] !== cid); if (miss) return miss;
        if (spec.ordered) { const i = list.findIndex((id, k) => have[k] !== id); if (i >= 0) return list[i]; }
      }
      return null;
    };
    const mark = (list, cls) => { if (list.length && cv.mark) cv.mark(list, cls); };
    const placeAll = (v, o) => Object.entries(v || {}).forEach(([cid, list]) => (list || []).forEach(id => cv.place(id, cid, o)));
    return {
      el,
      value: () => contents(),
      set(v) { placeAll(v); moved = true; ctx.change && ctx.change({ set: true }); },
      /* the authored answer; with count only, the first n items not yet there are moved into each counted container */
      answer: () => {
        if (Object.keys(want).length || !spec.count) return JSON.parse(JSON.stringify(want));
        const c = contents(), out = {}, used = new Set();
        Object.entries(spec.count).forEach(([cid, n]) => { const have = (c[cid] || []).slice(0, +n); have.forEach(id => used.add(id)); out[cid] = have; });
        Object.entries(spec.count).forEach(([cid, n]) => { const pool = Object.entries(c).filter(([k]) => !(k in spec.count)).flatMap(([, l]) => l).filter(id => !used.has(id)); while (out[cid].length < +n && pool.length) { const id = pool.shift(); used.add(id); out[cid].push(id); } });
        return out;
      },
      ready: () => moved,
      dirty: () => moved,
      grade() { const k = misplaced(); return { ok: !k, key: k, detail: { contents: contents() } }; },
      lock() { cv.lock && cv.lock(true); },
      unlock() { cv.lock && cv.lock(false); cv.unmark && cv.unmark(); },
      markGraded(res) {
        cv.unmark && cv.unmark();
        const w = where(), named = Object.entries(want).flatMap(([cid, list]) => list.map(id => [id, cid]));
        const inNamed = Object.entries(contents()).filter(([cid]) => cid in want).flatMap(([cid, list]) => list.map(id => [id, cid]));
        const good = named.filter(([id, cid]) => w[id] === cid).map(([id]) => id);
        const bad = inNamed.filter(([id, cid]) => !(want[cid] || []).includes(id)).map(([id]) => id);
        mark(good, res && res.ok ? 'is-correct' : 'is-dim'); mark(bad, 'is-notyet');
      },
      reveal() { cv.unmark && cv.unmark(); placeAll(Object.keys(want).length ? want : this.answer()); mark(Object.values(want).flat(), 'is-reveal'); cv.lock && cv.lock(true); },
      reset() { cv.unmark && cv.unmark(); cv.lock && cv.lock(false); cv.set({ move: null, draw: [] }, { instant: true }); placeAll(start, { instant: true }); moved = false; },
      focus() { const n = cv.el.querySelector('.cv-handle[tabindex="0"]'); if (n) n.focus({ preventScroll: true }); },
      destroy() { if (cv.enable) cv.enable(null); },
    };
  };

  /* item 411, mode "array": the learner drags the cells of the screen's array canvas into order; answer lists the cell
     ids (c0, c1, ... by opening index) in the order wanted; key = the first id out of place */
  const arrayMode = (host, spec, ctx) => {
    const cv = ctx.canvas;
    const el = Z.h('<div class="wd-drag"><p class="t-caption wd-drag-msg" hidden></p></div>');
    host.append(el);
    const msg = el.querySelector('.wd-drag-msg');
    if (!cv || typeof cv.order !== 'function' || typeof cv.setOrder !== 'function') { msg.hidden = false; msg.textContent = 'This task needs its array diagram, which could not be drawn.'; return { el, value: () => [], grade: () => ({ ok: false, key: null, detail: null }) }; }
    const want = (spec.answer || []).map(String), start = cv.order();
    let moved = false;
    cv.enable('drag', {});
    cv.on('change', (e) => { if (e && e.type === 'order') { moved = true; ctx.change && ctx.change({ order: e.order }); } });
    const firstOff = () => { const o = cv.order(); const i = want.findIndex((id, k) => o[k] !== id); return i < 0 ? null : want[i]; };
    return {
      el,
      value: () => cv.order(),
      set(v) { cv.setOrder(v); moved = true; ctx.change && ctx.change({ set: true }); },
      answer: () => want.slice(),
      ready: () => moved,
      dirty: () => moved,
      grade() { const k = firstOff(); return { ok: !k, key: k, detail: { order: cv.order() } }; },
      lock() { cv.lock && cv.lock(true); },
      unlock() { cv.lock && cv.lock(false); cv.unmark && cv.unmark(); },
      markGraded(res) { cv.unmark && cv.unmark(); const o = cv.order(); if (!cv.mark) return; const at = (id) => 'c' + (o.indexOf(id) + (cv.params && cv.params.indexFrom || 0)); const good = want.filter((id, k) => o[k] === id).map(at), bad = want.filter((id, k) => o[k] !== id).map(at); if (good.length) cv.mark(good, res && res.ok ? 'is-correct' : 'is-dim'); if (bad.length) cv.mark(bad, 'is-notyet'); },
      reveal() { cv.unmark && cv.unmark(); cv.setOrder(want, {}); cv.lock && cv.lock(true); },
      reset() { cv.unmark && cv.unmark(); cv.lock && cv.lock(false); cv.setOrder(start); moved = false; },
      focus() { const n = cv.el.querySelector('[data-drag]'); if (n) n.focus({ preventScroll: true }); },
      destroy() { if (cv.enable) cv.enable(null); },
    };
  };

  Z.widgets.register('place', (host, spec, ctx) => {
    if (spec.mode === 'boxes') return boxesMode(host, spec, ctx);
    if (spec.mode === 'array') return arrayMode(host, spec, ctx);
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

    /* Interchangeable tokens: a group key per token (its text with byText, its `same` group, else its own id) */
    const groups = Array.isArray(spec.same) && spec.same.length ? (Array.isArray(spec.same[0]) ? spec.same : [spec.same]) : [];
    const gkey = (id) => {
      if (spec.byText) return 't:' + String((tokById[id] || {}).text ?? id).replace(/\s+/g, ' ').trim();
      const g = groups.findIndex(list => list.includes(id)); return g >= 0 ? 'g:' + g : 'i:' + id;
    };
    const strip = () => el.querySelectorAll('.wd-tok').forEach(n => { n.classList.remove('ok', 'bad', 'wd-rev', 'dim'); n.querySelector('.wd-tok-mark').innerHTML = ''; });
    const home = Object.fromEntries(tokens.map(t => [t.id, 'bank']));
    if (mode === 'assign') slots.forEach(s => (s.accepts || []).forEach(id => { home[id] = s.id; }));
    /* Per token, right or not: a slot (or a position) takes a token whose group it still needs */
    const verdicts = () => {
      const v = value(), out = {};
      if (mode === 'order') { const want = spec.order || []; v.forEach((id, k) => { out[id] = want[k] != null && gkey(want[k]) === gkey(id); }); return out; }
      const need = {};
      tokens.forEach(t => { const h = home[t.id]; need[h] = need[h] || {}; need[h][gkey(t.id)] = (need[h][gkey(t.id)] || 0) + 1; });
      const where = {}; tokens.forEach(t => { where[t.id] = 'bank'; });
      Object.entries(v).forEach(([sl, list]) => list.forEach(id => { where[id] = sl; }));
      [...el.querySelectorAll('.wd-tok')].map(n => n.dataset.id).forEach(id => {
        const n = need[where[id]] || {}, k = gkey(id);
        if (n[k] > 0) { n[k]--; out[id] = true; } else out[id] = false;
      });
      return out;
    };
    const misplaced = () => {
      const v = value();
      if (mode === 'order') {
        const want = spec.order || [], ok = verdicts();
        const i = v.findIndex(id => !ok[id]);
        if (i >= 0) return v[i];
        if (v.length < want.length) return want[v.length];
        return null;
      }
      const ok = verdicts();
      // order of checking: tokens in the order they appear on screen
      const seen = [...el.querySelectorAll('.wd-tok')].map(n => n.dataset.id);
      return seen.find(id => !ok[id]) || null;
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
        const v = value(), ok = verdicts();
        const where = {};
        if (mode === 'order') v.forEach((id) => { where[id] = ok[id]; });
        else Object.values(v).forEach(list => list.forEach(id => { where[id] = ok[id]; }));
        Object.entries(where).forEach(([id, ok]) => { const n = tokEl(id); n.classList.add(res.ok || ok ? 'ok' : 'bad'); n.querySelector('.wd-tok-mark').innerHTML = Z.icon(res.ok || ok ? 'check' : 'cross'); });
      },
      reveal() { setValue(correct()); strip(); locked = true; el.classList.add('is-locked'); el.querySelectorAll('.wd-slot .wd-tok').forEach(n => n.classList.add('wd-rev')); el.querySelectorAll('.wd-bank .wd-tok').forEach(n => n.classList.add('dim')); },
      reset() { strip(); locked = false; el.classList.remove('is-locked'); setValue(mode === 'order' ? [] : {}); },
      focus() { el.querySelector('.wd-tok')?.focus({ preventScroll: true }); },
      destroy() { drag = null; },
    };
  });
})();
