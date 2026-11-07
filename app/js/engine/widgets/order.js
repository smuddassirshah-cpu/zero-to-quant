/* Order-the-steps widget (docs/AUTHORING.md 3, design-research 5.3 nos. 7 and 15).
   Lines are shuffled on render. Each line is a lipped token: drag it (a lifted token scales to 1.03, drops its lip
   and takes the e2 shadow; siblings slide aside over 200ms; the drop snaps on spring-snap), or use the keyboard:
   Space lifts, arrows move, Space drops, Escape puts it back. Exact order; per-line marks after grading.
   same: [[ids]] makes lines interchangeable among their places (item 201).
   distractors: [ids] (item 434): lines that must be left out. Every line has a button that moves it to a "Left out"
   list below and back; answer lists only the lines that belong. Grading: a distractor in the sequence returns its id
   as the key (and its text's why, if any, as the line), a needed line left out returns "left-out", else the first
   misplaced line's id as before. Without distractors the widget is unchanged. */
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

  const OUT_BTN = `<button type="button" class="icon-btn wd-line-out" aria-label="Leave this line out" title="Leave out" style="flex:none;width:32px;height:32px;margin:-4px -6px -4px 4px"><svg class="icon sm" viewBox="0 0 24 24" aria-hidden="true"><path d="M7 7l10 10M17 7L7 17"/></svg></button>`;
  const BACK_BTN = `<svg class="icon sm" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 5v14M5 12h14"/></svg>`;

  Z.widgets.register('order', (host, spec, ctx) => {
    const lines = spec.lines || [];
    const byId = Object.fromEntries(lines.map(l => [l.id, l]));
    const dis = new Set((Array.isArray(spec.distractors) ? spec.distractors : []).map(String));
    const answer = (spec.answer || lines.filter(l => !dis.has(String(l.id))).map(l => l.id)).slice();
    const dline = (id) => (dis.size && dis.has(String(id)) ? (byId[id] && byId[id].why) || null : null);
    /* item 201: same: [["s2", "s3"]] makes lines interchangeable among their places (independent steps) */
    const groups = Array.isArray(spec.same) && spec.same.length ? (Array.isArray(spec.same[0]) ? spec.same : [spec.same]) : [];
    const gk = (id) => { const k = groups.findIndex(g => g.map(String).includes(String(id))); return k >= 0 ? '\u0000g' + k : id; };
    const sameOrder = (a, b) => a.length === b.length && a.every((id, i) => gk(id) === gk(b[i]));
    /* ENGINE-BACKLOG 616: after: { "d4": ["d2", "d3"] } is a set of precedence rules: any order in which every listed line comes after the lines it names is
       correct (a proof whose two independent lemmas may come either way round). The model order in `answer` must satisfy the rules; `same` is ignored when `after` is set. */
    const after = spec.after && typeof spec.after === 'object' && !Array.isArray(spec.after) ? spec.after : null;
    const preds = (id) => (after && Array.isArray(after[id]) ? after[id].map(String) : []);
    const late = (arr, id, i) => preds(id).some(q => { const k = arr.map(String).indexOf(q); return k < 0 || k > i; });   // a named line is missing or comes later
    const orderOk = (arr) => (after ? arr.length === answer.length && answer.every(id => arr.map(String).includes(String(id))) && !arr.some((id, i) => late(arr, id, i)) : sameOrder(arr, answer));
    let start = Z.widgets.shuffle(dis.size ? lines.map(l => l.id) : answer, ctx.rng || Math.random);
    if (start.length > 1 && orderOk(start)) start = start.slice(1).concat(start[0]); // never start solved
    const el = Z.h(`<div class="wd-order">
      <ol class="wd-lines" role="listbox" aria-label="${Z.esc(spec.label || 'Lines to put in order')}" aria-describedby="">${start.map((id, i) => `
        <li class="wd-line wd-tok" role="option" tabindex="${i === 0 ? 0 : -1}" aria-selected="false" data-id="${Z.esc(id)}">
          <span class="wd-grip" aria-hidden="true"><i></i><i></i><i></i></span>
          <span class="wd-line-n tnum" aria-hidden="true"></span>
          <span class="wd-line-tx">${Z.grade.inline(byId[id]?.text ?? id)}</span>
          <span class="wd-line-mark" aria-hidden="true"></span>${dis.size ? OUT_BTN : ''}
        </li>`).join('')}</ol>${dis.size ? `
      <div class="wd-spare-wrap" style="margin-top:16px">
        <p class="t-overline muted" style="margin:0 0 8px">Left out</p>
        <ol class="wd-lines wd-spare" aria-label="Lines left out"></ol>
        <p class="t-caption wd-spare-empty" style="margin:0;color:var(--text-muted)">Lines that do not belong go here.</p>
      </div>` : ''}
      <p class="t-caption wd-order-help">Drag a line, or focus it and press Space, then the arrow keys, then Space.${dis.size ? ' Some lines do not belong: press the cross on a line (or Delete) to leave it out.' : ''}</p>
      <p class="sr-only" aria-live="assertive"></p>
    </div>`);
    host.append(el);
    const list = el.querySelector('.wd-lines'), live = el.querySelector('[aria-live]');
    const spare = el.querySelector('.wd-spare'), spareEmpty = el.querySelector('.wd-spare-empty');
    const items = () => [...list.children];
    const spareItems = () => (spare ? [...spare.children] : []);
    const ids = () => items().map(n => n.dataset.id);
    const out = () => spareItems().map(n => n.dataset.id);
    const number = () => {
      items().forEach((n, i) => { const b = n.querySelector('.wd-line-n'); b.textContent = i + 1; b.style.display = ''; n.querySelector('.wd-grip').style.display = ''; n.style.cursor = ''; });
      spareItems().forEach(n => { n.querySelector('.wd-line-n').style.display = 'none'; n.querySelector('.wd-grip').style.display = 'none'; n.style.cursor = 'default'; }); // left-out lines are not draggable
      if (spareEmpty) spareEmpty.hidden = spareItems().length > 0;
    };
    number();
    let locked = false, lifted = null, liftFrom = -1;
    const say = (t) => { live.textContent = t; };
    const changed = () => { number(); ctx.change && ctx.change({ order: ids(), out: out() }); };
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
    /* item 434: the cross on a line moves it to the Left out list; the plus on a left-out line puts it back at the end */
    const toggleOut = (n) => {
      if (locked) return;
      if (lifted) drop(false);
      const to = n.parentNode === list ? spare : list, btn = n.querySelector('.wd-line-out');
      to.append(n);
      n.classList.toggle('dim', to === spare);
      btn.innerHTML = to === spare ? BACK_BTN : '<svg class="icon sm" viewBox="0 0 24 24" aria-hidden="true"><path d="M7 7l10 10M17 7L7 17"/></svg>';
      btn.setAttribute('aria-label', to === spare ? 'Put this line back' : 'Leave this line out');
      btn.title = to === spare ? 'Put back' : 'Leave out';
      n.setAttribute('tabindex', '-1');
      if (to === list && !items().some(x => x.getAttribute('tabindex') === '0')) n.setAttribute('tabindex', '0');
      say(to === spare ? 'Line left out.' : 'Line put back at the end.');
      changed();
      btn.focus();
    };
    if (spare) el.addEventListener('click', (e) => { const b = e.target.closest('.wd-line-out'); if (b) toggleOut(b.closest('.wd-line')); });
    list.addEventListener('keydown', (e) => {
      if (e.target.closest('.wd-line-out')) return; // Space and Enter on the button press it
      const n = e.target.closest('.wd-line'); if (!n || locked) return;
      if (e.key === ' ') { e.preventDefault(); if (lifted) drop(false); else lift(n); return; }
      if (spare && (e.key === 'Delete' || e.key === 'Backspace')) { e.preventDefault(); toggleOut(n); return; }
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
      const n = e.target.closest('.wd-line'); if (!n || locked || e.button !== 0 || e.target.closest('.wd-line-out')) return;
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

    const everyItem = () => items().concat(spareItems());
    /* once graded or revealed, the marks replace the leave-out buttons */
    const outBtns = (hide) => el.querySelectorAll('.wd-line-out').forEach(b => { b.disabled = hide; b.style.display = hide ? 'none' : ''; });
    const strip = () => everyItem().forEach(n => { n.classList.remove('ok', 'bad', 'wd-rev'); n.classList.toggle('dim', n.parentNode === spare); n.querySelector('.wd-line-mark').innerHTML = ''; });
    /* put a line in the list it belongs to and set its button to match */
    const home = (n, toSpare) => {
      const to = toSpare ? spare : list; if (n.parentNode !== to) to.append(n);
      const b = n.querySelector('.wd-line-out'); if (!b) return;
      b.innerHTML = toSpare ? BACK_BTN : '<svg class="icon sm" viewBox="0 0 24 24" aria-hidden="true"><path d="M7 7l10 10M17 7L7 17"/></svg>';
      b.setAttribute('aria-label', toSpare ? 'Put this line back' : 'Leave this line out'); b.title = toSpare ? 'Put back' : 'Leave out';
    };
    const setOrder = (order, animate = true) => {
      const all = items(), map = Object.fromEntries(everyItem().map(n => [n.dataset.id, n]));
      /* with distractors, a line missing from order goes to the Left out list */
      const doIt = () => { if (spare) { const set = new Set(order.map(String)); everyItem().forEach(n => { if (!set.has(n.dataset.id)) home(n, true); }); } order.forEach(id => { if (map[id]) { home(map[id], false); list.append(map[id]); } }); };
      if (animate) flip(all, doIt, 600); else doIt();
      strip();
      number();
    };
    return {
      el,
      value: ids,
      set(v) { if (Array.isArray(v)) { setOrder(v, false); changed(); } },
      answer: () => answer.slice(),
      ready: () => true,
      dirty: () => !Z.grade.sameList(ids(), start) || spareItems().length > 0,
      grade() {
        const cur = ids();
        const ok = orderOk(cur);
        let first = after ? cur.find((id, i) => late(cur, id, i)) : cur.find((id, i) => gk(id) !== gk(answer[i])), line;
        if (!ok && dis.size) {
          const bad = cur.find(id => dis.has(String(id)));
          if (bad != null) { first = bad; line = dline(bad) || 'One of those lines does not belong in the sequence.'; }
          else if (answer.some(id => !cur.includes(id))) { first = 'left-out'; line = 'A line that belongs is in the Left out list.'; }
        }
        return { ok, key: ok ? null : first || null, line, detail: { order: cur, out: out() } };
      },
      lock() { locked = true; drop(false); list.classList.add('is-locked'); if (spare) spare.classList.add('is-locked'); outBtns(true); },
      unlock() { locked = false; list.classList.remove('is-locked'); if (spare) spare.classList.remove('is-locked'); outBtns(false); strip(); },
      markGraded(res) {
        strip();
        const mark = (n, ok) => { n.classList.remove('dim'); n.classList.add(ok ? 'ok' : 'bad'); n.querySelector('.wd-line-mark').innerHTML = Z.icon(ok ? 'check' : 'cross'); };
        const nowIds = items().map(n => n.dataset.id);
        items().forEach((n, i) => mark(n, after ? answer.map(String).includes(n.dataset.id) && !late(nowIds, n.dataset.id, i) : answer[i] != null && !dis.has(n.dataset.id) && gk(n.dataset.id) === gk(answer[i])));
        spareItems().forEach(n => mark(n, dis.has(n.dataset.id))); // a left-out line is right exactly when it is a distractor
      },
      reveal() { locked = true; strip(); setOrder(answer, true); everyItem().forEach(n => n.classList.add('wd-rev')); list.classList.add('is-locked'); if (spare) spare.classList.add('is-locked'); outBtns(true); },
      reset() { locked = false; list.classList.remove('is-locked'); if (spare) spare.classList.remove('is-locked'); outBtns(false); strip(); if (spare) everyItem().forEach(n => home(n, false)); setOrder(start, true); changed(); },
      focus() { items()[0]?.focus({ preventScroll: true }); },
      destroy() { drag = null; },
    };
  });
})();
