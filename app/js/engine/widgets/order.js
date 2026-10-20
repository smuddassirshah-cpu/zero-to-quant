/* Order-the-steps widget (docs/AUTHORING.md 3, design-research 5.3 nos. 7 and 15).
   Lines are shuffled on render. Each line is a lipped token: drag it (a lifted token scales to 1.03, drops its lip
   and takes the e2 shadow; siblings slide aside over 200ms; the drop snaps on spring-snap), or use the keyboard:
   Space lifts, arrows move, Space drops, Escape puts it back. Exact order; per-line marks after grading. */
(function () {
  'use strict';
  const Z = window.ZQ;

  /* FLIP: animate elements from their old boxes to their new ones */
  const flip = (els, mutate, ms = 200) => {
    const before = new Map(els.map(e => [e, e.getBoundingClientRect().top]));
    mutate();
    if (Z.reducedMotion()) return;
    els.forEach(e => {
      const dy = before.get(e) - e.getBoundingClientRect().top;
      if (Math.abs(dy) < 0.5 || e.classList.contains('is-dragging')) return;
      e.animate([{ transform: `translateY(${dy}px)` }, { transform: 'none' }], { duration: ms, easing: 'cubic-bezier(0.2, 0, 0, 1)' });
    });
  };

  Z.widgets.register('order', (host, spec, ctx) => {
    const lines = spec.lines || [];
    const byId = Object.fromEntries(lines.map(l => [l.id, l]));
    const answer = (spec.answer || lines.map(l => l.id)).slice();
    /* item 201: same: [["s2", "s3"]] makes lines interchangeable among their places (independent steps) */
    const groups = Array.isArray(spec.same) && spec.same.length ? (Array.isArray(spec.same[0]) ? spec.same : [spec.same]) : [];
    const gk = (id) => { const k = groups.findIndex(g => g.map(String).includes(String(id))); return k >= 0 ? '\u0000g' + k : id; };
    const sameOrder = (a, b) => a.length === b.length && a.every((id, i) => gk(id) === gk(b[i]));
    let start = Z.widgets.shuffle(answer, ctx.rng || Math.random);
    if (start.length > 1 && sameOrder(start, answer)) start = start.slice(1).concat(start[0]); // never start solved
    const el = Z.h(`<div class="wd-order">
      <ol class="wd-lines" role="listbox" aria-label="${Z.esc(spec.label || 'Lines to put in order')}" aria-describedby="">${start.map((id, i) => `
        <li class="wd-line wd-tok" role="option" tabindex="${i === 0 ? 0 : -1}" aria-selected="false" data-id="${Z.esc(id)}">
          <span class="wd-grip" aria-hidden="true"><i></i><i></i><i></i></span>
          <span class="wd-line-n tnum" aria-hidden="true"></span>
          <span class="wd-line-tx">${Z.grade.inline(byId[id]?.text ?? id)}</span>
          <span class="wd-line-mark" aria-hidden="true"></span>
        </li>`).join('')}</ol>
      <p class="t-caption wd-order-help">Drag a line, or focus it and press Space, then the arrow keys, then Space.</p>
      <p class="sr-only" aria-live="assertive"></p>
    </div>`);
    host.append(el);
    const list = el.querySelector('.wd-lines'), live = el.querySelector('[aria-live]');
    const items = () => [...list.children];
    const ids = () => items().map(n => n.dataset.id);
    const number = () => items().forEach((n, i) => { n.querySelector('.wd-line-n').textContent = i + 1; });
    number();
    let locked = false, lifted = null, liftFrom = -1;
    const say = (t) => { live.textContent = t; };
    const changed = () => { number(); ctx.change && ctx.change({ order: ids() }); };
    const focusItem = (n) => { items().forEach(x => x.setAttribute('tabindex', x === n ? '0' : '-1')); n.focus({ preventScroll: false }); };
    const move = (n, to) => {
      const all = items(), from = all.indexOf(n);
      to = Math.max(0, Math.min(all.length - 1, to));
      if (to === from) return;
      flip(all, () => { const ref = to > from ? all[to].nextSibling : all[to]; list.insertBefore(n, ref); });
      changed();
    };
    const lift = (n) => { lifted = n; liftFrom = items().indexOf(n); n.classList.add('is-lifted'); n.setAttribute('aria-selected', 'true'); say(`Lifted line ${liftFrom + 1}. Use the arrow keys, then Space to drop.`); };
    const drop = (cancel) => {
      if (!lifted) return;
      const n = lifted; lifted = null;
      if (cancel) move(n, liftFrom);
      n.classList.remove('is-lifted'); n.setAttribute('aria-selected', 'false');
      if (!Z.reducedMotion()) n.animate([{ transform: 'scale(1.03)' }, { transform: 'none' }], { duration: 300, easing: getComputedStyle(document.documentElement).getPropertyValue('--spring-snap').trim() || 'ease-out' });
      say(`Dropped at position ${items().indexOf(n) + 1}.`);
      Z.sound('tap');
    };
    list.addEventListener('keydown', (e) => {
      const n = e.target.closest('.wd-line'); if (!n || locked) return;
      if (e.key === ' ') { e.preventDefault(); if (lifted) drop(false); else lift(n); return; }
      if (e.key === 'Escape' && lifted) { e.preventDefault(); e.stopPropagation(); drop(true); focusItem(n); return; }
      const d = { ArrowUp: -1, ArrowDown: 1, ArrowLeft: -1, ArrowRight: 1 }[e.key];
      if (!d) return;
      e.preventDefault();
      const all = items(), i = all.indexOf(n);
      if (lifted === n) { move(n, i + d); focusItem(n); say(`Position ${items().indexOf(n) + 1}.`); }
      else if (all[i + d]) focusItem(all[i + d]);
    });
    list.addEventListener('focusout', (e) => { if (lifted && !list.contains(e.relatedTarget)) drop(false); });

    /* Pointer drag: the line follows the pointer; crossing a sibling's centre reorders with FLIP */
    let drag = null;
    list.addEventListener('pointerdown', (e) => {
      const n = e.target.closest('.wd-line'); if (!n || locked || e.button !== 0) return;
      drag = { n, y0: e.clientY, dy: 0, on: false, id: e.pointerId };
      n.setPointerCapture(e.pointerId);
    });
    list.addEventListener('pointermove', (e) => {
      if (!drag || e.pointerId !== drag.id) return;
      const d = drag;
      d.dy = e.clientY - d.y0;
      if (!d.on) { if (Math.abs(d.dy) < 4) return; d.on = true; d.n.classList.add('is-lifted', 'is-dragging'); }
      d.n.style.transform = `translateY(${d.dy}px) scale(1.03)`;
      const all = items(), i = all.indexOf(d.n), r = d.n.getBoundingClientRect(), mid = r.top + r.height / 2;
      const prev = all[i - 1], next = all[i + 1];
      const centre = (x) => { const b = x.getBoundingClientRect(); return b.top + b.height / 2; };
      let target = null;
      if (next && mid > centre(next)) target = next;
      else if (prev && mid < centre(prev)) target = prev;
      if (target) {
        const top0 = d.n.offsetTop;
        flip(all, () => list.insertBefore(d.n, target === next ? next.nextSibling : prev));
        const shift = d.n.offsetTop - top0;
        d.y0 += shift; d.dy -= shift;
        d.n.style.transform = `translateY(${d.dy}px) scale(1.03)`;
        changed();
      }
    });
    const end = (e) => {
      if (!drag || e.pointerId !== drag.id) return;
      const d = drag; drag = null;
      if (!d.on) return;
      d.n.classList.remove('is-dragging');
      const from = `translateY(${d.dy}px) scale(1.03)`;
      d.n.style.transform = '';
      d.n.classList.remove('is-lifted');
      if (!Z.reducedMotion()) d.n.animate([{ transform: from }, { transform: 'none' }], { duration: 300, easing: getComputedStyle(document.documentElement).getPropertyValue('--spring-snap').trim() || 'ease-out' });
      Z.sound('tap'); changed();
    };
    list.addEventListener('pointerup', end); list.addEventListener('pointercancel', end);

    const strip = () => items().forEach(n => { n.classList.remove('ok', 'bad', 'wd-rev', 'dim'); n.querySelector('.wd-line-mark').innerHTML = ''; });
    const setOrder = (order, animate = true) => {
      const all = items(), map = Object.fromEntries(all.map(n => [n.dataset.id, n]));
      const doIt = () => order.forEach(id => map[id] && list.append(map[id]));
      if (animate) flip(all, doIt, 600); else doIt();
      number();
    };
    return {
      el,
      value: ids,
      set(v) { if (Array.isArray(v)) { setOrder(v, false); changed(); } },
      answer: () => answer.slice(),
      ready: () => true,
      dirty: () => !Z.grade.sameList(ids(), start),
      grade() {
        const cur = ids();
        const ok = sameOrder(cur, answer);
        const first = cur.find((id, i) => gk(id) !== gk(answer[i]));
        return { ok, key: ok ? null : first || null, detail: { order: cur } };
      },
      lock() { locked = true; drop(false); list.classList.add('is-locked'); },
      unlock() { locked = false; list.classList.remove('is-locked'); strip(); },
      markGraded(res) {
        strip();
        items().forEach((n, i) => {
          const ok = gk(n.dataset.id) === gk(answer[i]);
          n.classList.add(ok ? 'ok' : 'bad');
          n.querySelector('.wd-line-mark').innerHTML = Z.icon(ok ? 'check' : 'cross');
        });
      },
      reveal() { locked = true; strip(); setOrder(answer, true); items().forEach(n => n.classList.add('wd-rev')); list.classList.add('is-locked'); },
      reset() { locked = false; list.classList.remove('is-locked'); strip(); setOrder(start, true); changed(); },
      focus() { items()[0]?.focus({ preventScroll: true }); },
      destroy() { drag = null; },
    };
  });
})();
