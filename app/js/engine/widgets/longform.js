/* Long-form answer with self-marking (docs/AUTHORING.md 5, the homework flow from the prototype's review.js).
   Phase 1: a textarea for the working (maths in $...$ is previewed). The first Check does not grade: grade()
   returns { pending: true } and the widget opens the self-marking panel (the working locks, the model answer and
   the rubric appear, one tick box per criterion, points summing to 10). Phase 2: Check grades the self-mark;
   ok when it is 7 or more. Spec fields: prompt (optional, shown above), model (markdown with KaTeX), rubric[].
   The help line names the button that opens the marking: "Check" in set mode, "Mark my answer" in exam mode (the
   homework page, which renders items in exam mode, has a Mark my answer button under each written item).
   Performance task (ENGINE-BACKLOG 529): spec.seconds makes it an aloud answer (a clock with a Start button, a guide that never locks, the box is
   optional notes) and spec.followUps lists the interviewer's next questions, shown with the model answer; spec.data adds the data panel.
   Provenance (N01): grade() carries how: 'self'; result rows for longform items are stored as self and never reach
   the mastery map or a prerequisite (docs/AUTHORING.md, Result provenance). */
(function () {
  'use strict';
  const Z = window.ZQ;
  const PASS = 7;

  Z.widgets.register('longform', (host, spec, ctx) => {
    const rubric = spec.rubric || [], destroyers = [];
    const fmt = (n) => `${Math.floor(n / 60)}:${String(n % 60).padStart(2, '0')}`;
    const total = rubric.reduce((a, r) => a + (+r.points || 0), 0) || 10;
    const el = Z.h(`<div class="wd-long">
      <div class="wd-long-write">
        <label class="t-label" for="">Your working</label>
        <textarea class="wd-long-ta" rows="8" spellcheck="true" placeholder="Write each step and the reason for it."></textarea>
        <p class="t-caption muted">Wrap maths in dollar signs to typeset it in the preview. ${ctx.mode === 'exam' ? 'Mark my answer' : 'Check'} opens the model answer so you can mark your own work.</p>
        <div class="wd-long-prev" hidden><span class="t-overline muted">Preview</span><div class="t-body wd-long-prev-b"></div></div>
      </div>
      <div class="wd-long-mark" hidden>
        <div class="wd-long-mine"><span class="t-overline muted">Your working, locked</span><div class="t-body wd-long-mine-b"></div></div>
        <div class="wd-long-model"><h3 class="t-h2">Model answer</h3><div class="wd-long-model-b">${Z.grade.prose(spec.model || '', 't-body')}</div></div>
        <fieldset class="wd-rubric">
          <legend class="t-h2">Mark it out of ${total}</legend>
          <p class="t-caption secondary">Tick each point your working shows. Be strict. This mark is your own, so it shows under Self-marked and never moves your mastery map. ${PASS} or more counts as right${rubric.some(r => r.required) ? ', and every row marked required must be ticked' : ''}.</p>
          <div class="wd-rbs">${rubric.map((r, k) => `<label class="wd-rb"><input type="checkbox" data-rb="${k}"><span class="wd-box" aria-hidden="true">${Z.icon('check')}</span><span class="t-body">${Z.grade.inline(r.text)}</span><span class="wd-rb-pts t-caption tnum">${r.points} ${+r.points === 1 ? 'point' : 'points'}${r.required ? ', required' : ''}</span></label>`).join('')}</div>
          <div class="wd-score" aria-live="polite"><span class="t-stat tnum" data-score>0</span><span class="t-h2 muted">of ${total}</span></div>
        </fieldset>
      </div>
    </div>`);
    const aloud = Number(spec.seconds) > 0, follow = Array.isArray(spec.followUps) ? spec.followUps : [];
    if (aloud) {
      el.querySelector('label.t-label').textContent = 'Your notes (optional)';
      el.querySelector('.wd-long-ta').placeholder = 'Jot the points you will say. You can leave this empty.';
      const clock = Z.h(`<div class="wd-long-clock"><span class="t-stat tnum" data-clock>${fmt(spec.seconds)}</span><button type="button" class="btn secondary" data-clock-go>Start the clock</button><span class="t-caption muted">Say your answer aloud. The clock is a guide and never stops you. The box is for notes and is optional.</span></div>`);
      el.querySelector('.wd-long-write').prepend(clock);
      const out = clock.querySelector('[data-clock]'), go = clock.querySelector('[data-clock-go]');
      let t0 = 0, iv = null;
      const tick = () => { const left = Math.round(spec.seconds - (Date.now() - t0) / 1000); out.textContent = (left < 0 ? '-' : '') + fmt(Math.abs(left)); clock.classList.toggle('is-over', left < 0); };
      go.addEventListener('click', () => { if (iv) { clearInterval(iv); iv = null; go.textContent = 'Start the clock'; out.textContent = fmt(spec.seconds); clock.classList.remove('is-over'); return; } t0 = Date.now(); iv = setInterval(tick, 500); go.textContent = 'Stop'; tick(); });
      destroyers.push(() => { if (iv) clearInterval(iv); });
    }
    if (follow.length) el.querySelector('.wd-long-model').insertAdjacentHTML('beforebegin', `<div class="wd-long-follow"><h3 class="t-h2">Follow-ups</h3><p class="t-caption secondary">An interviewer would ask these next. Answer each aloud before you read the model answer.</p><ol class="t-body">${follow.map(f => `<li>${Z.grade.inline(f)}</li>`).join('')}</ol></div>`);
    const dp = Z.widgets.dataPanel(spec); if (dp) el.prepend(dp);   // performance task "data": the file to read
    host.append(el);
    const id = 'wd-long-' + Math.random().toString(36).slice(2, 8);
    const ta = el.querySelector('.wd-long-ta'); ta.id = id; el.querySelector('label.t-label').setAttribute('for', id);
    const prev = el.querySelector('.wd-long-prev'), prevB = el.querySelector('.wd-long-prev-b');
    const write = el.querySelector('.wd-long-write'), markP = el.querySelector('.wd-long-mark');
    const boxes = [...el.querySelectorAll('[data-rb]')];
    let phase = 'write', locked = false;
    const score = () => boxes.reduce((a, b) => a + (b.checked ? +rubric[+b.dataset.rb].points || 0 : 0), 0);
    const ticks = () => boxes.filter(b => b.checked).map(b => +b.dataset.rb);
    const syncScore = () => { el.querySelector('[data-score]').textContent = score(); };
    const typeset = (s) => Z.grade.prose(s, 't-body');
    const upd = () => { prev.hidden = !ta.value.includes('$'); prevB.innerHTML = typeset(ta.value); };
    ta.addEventListener('input', () => { upd(); ctx.change && ctx.change({ text: ta.value }); });
    boxes.forEach(b => b.addEventListener('change', () => { syncScore(); Z.sound('tap'); ctx.change && ctx.change({ ticks: ticks() }); }));
    const toMark = () => {
      phase = 'mark';
      el.querySelector('.wd-long-mine-b').innerHTML = ta.value.trim() ? typeset(ta.value) : '<span class="muted">No working written.</span>';
      write.hidden = true; markP.hidden = false;
      const m = el.querySelector('.wd-long-model');
      if (m && m.scrollIntoView) m.scrollIntoView({ behavior: Z.reducedMotion() ? 'auto' : 'smooth', block: 'start' });
    };
    const setLock = (v) => { locked = v; ta.readOnly = v; boxes.forEach(b => { b.disabled = v; }); };
    return {
      el,
      value: () => ({ text: ta.value, ticks: ticks(), marked: phase === 'mark', score: score() }),
      set(v) {
        if (!v) return;
        if (typeof v === 'string') { ta.value = v; upd(); }
        else {
          if (v.text != null) { ta.value = v.text; upd(); }
          if (v.marked || v.ticks) { toMark(); boxes.forEach(b => { b.checked = (v.ticks || []).includes(+b.dataset.rb); }); syncScore(); }
        }
        ctx.change && ctx.change(this.value());
      },
      answer: () => ({ text: 'I followed the model answer.', ticks: rubric.map((_, i) => i), marked: true }),
      ready: () => (phase === 'write' ? aloud || ta.value.trim() !== '' : true),
      dirty: () => ta.value !== '' || ticks().length > 0,
      grade() {
        if (phase === 'write') { toMark(); return { pending: true, ok: false, key: null }; }
        const s = score(), ticked = ticks(), lacks = rubric.some((r, k) => r.required && !ticked.includes(k)), pass = s >= PASS && !lacks;
        return { how: 'self', ok: pass, key: pass ? null : 'below', line: pass ? null : lacks && s >= PASS ? `You marked ${s} of ${total}, but a required point is missing. This one returns in your Redo queue.` : `You marked ${s} of ${total}. ${PASS} or more counts as right, so this one returns in your Redo queue.`, detail: { score: s, ticks: ticks(), text: ta.value } };
      },
      lock() { setLock(true); },
      unlock() { setLock(false); el.classList.remove('is-ok', 'is-bad'); },
      markGraded(r) { el.classList.toggle('is-ok', !!r.ok); el.classList.toggle('is-bad', !r.ok); },
      reveal() { toMark(); setLock(true); el.classList.add('wd-rev'); },
      reset() { phase = 'write'; ta.value = ''; upd(); boxes.forEach(b => { b.checked = false; }); syncScore(); write.hidden = false; markP.hidden = true; setLock(false); el.classList.remove('is-ok', 'is-bad', 'wd-rev'); },
      focus() { (phase === 'write' ? ta : boxes[0])?.focus({ preventScroll: true }); },
      destroy() { destroyers.forEach(f => f()); },
    };
  });
})();
