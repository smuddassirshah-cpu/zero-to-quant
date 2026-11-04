/* Prepare for (ENGINE-BACKLOG 455, docs/AUTHORING.md section 10): the lessons that prepare for an assessment, in study order.
   Routes: #prepare (the first path) and #prepare/<path id> (a path from content/prep.json, read through ZQ.content.prep*).
   Pick General, a stage with a role, or a firm; the page lists the path's steps with done, in progress or not yet written,
   must or should, the one-line why, and links to its mocks. A firm path says "Reported formats, as of <month year>".
   Paths do not unlock anything, but they follow the prerequisite locks (ENGINE-BACKLOG 487): a step whose lessons are all locked shows a lock and its first missing prerequisite, and a mock that names requires shows Locked.
   Learner state is read through ZQ.state; every selector carries the pp- prefix. */
(function () {
  'use strict';

  let onState = null;
  ZQ.on('state', (e) => { if (onState) onState(e); });

  const STAGES = ['oa', 'interview', 'superday'];
  const ROLES = [['trader', 'Trader'], ['research', 'Research'], ['strats', 'Strats'], ['developer', 'Developer']];
  const roleName = (k) => (ROLES.find(r => r[0] === k) || [0, k])[1];

  ZQ.screen({
    id: 'prepare', title: 'Prepare for', group: 'App', shell: true, tab: 'learn',
    render(root, Z, params = []) {
      const C = Z.content, S = Z.state, esc = Z.esc;
      const paths = C.prepPaths();
      const plural = (n, one, many) => `${n} ${n === 1 ? one : many}`;
      let alive = true;

      if (!paths.length) {
        root.innerHTML = `<div class="pp"><div class="pp-empty card pad"><h1 class="t-h2">No preparation paths yet</h1>
          <p class="t-body secondary">They will appear here once they are written.</p><a class="btn secondary" href="#learn">Back to Learn</a></div></div>`;
        return null;
      }

      const generals = paths.filter(p => p.kind === 'general'), stagePaths = paths.filter(p => p.kind === 'stage'), firms = paths.filter(p => p.kind === 'firm');
      const modes = [['general', 'General', generals], ['stage', 'A stage', stagePaths], ['firm', 'A firm', firms]].filter(m => m[2].length);
      const asked = C.prepPath(params[0]);
      const sel = { mode: modes[0][0], general: (generals[0] || {}).id, stage: (stagePaths[0] || {}).stage || 'oa', role: (stagePaths[0] || {}).track || 'trader', firm: (firms[0] || {}).id };
      if (asked) {
        sel.mode = asked.kind;
        if (asked.kind === 'general') sel.general = asked.id;
        if (asked.kind === 'stage') { sel.stage = asked.stage; sel.role = asked.track; }
        if (asked.kind === 'firm') sel.firm = asked.id;
      }
      const current = () => (sel.mode === 'general' ? C.prepPath(sel.general) : sel.mode === 'firm' ? C.prepPath(sel.firm)
        : stagePaths.find(p => p.stage === sel.stage && p.track === sel.role) || null);

      /* ---------- Step facts ---------- */
      const done = (l) => { const r = S.lesson(l.course, l.id); return !!(r && r.done); };
      const started = (l) => { const r = S.lesson(l.course, l.id); return !!(r && (r.done || r.position)); };
      const stepState = (lessons) => {
        const w = lessons.filter(l => l.written === true);
        if (!w.length) return 'nw';
        if (w.every(done)) return w.length === lessons.length ? 'done' : 'prog';
        return w.some(started) ? 'prog' : 'todo';
      };
      const STATE = { done: ['Done', Z.icon('check', 'xs')], prog: ['In progress', '<i class="pp-dot is-half" aria-hidden="true"></i>'], todo: ['Not started', '<i class="pp-dot" aria-hidden="true"></i>'], nw: ['Not yet written', '<i class="pp-dot is-dash" aria-hidden="true"></i>'] };
      const stepTitle = (st) => {
        const [cid, rest] = st.ref.split('/');
        const c = C.course(cid) || { name: cid, levels: [] };
        if (rest == null) return { title: c.name, sub: 'Whole course' };
        const lv = /^level-(\d+)$/.exec(rest);
        if (lv) { const L = (c.levels || []).find(x => x.n === +lv[1]); return { title: c.name, sub: `Level ${lv[1]}${L && L.name ? `: ${L.name}` : ''}` }; }
        const l = st.lessons[0];
        return { title: l ? l.name : rest, sub: c.name };
      };
      /* Prerequisite gating (ENGINE-BACKLOG 487): a step whose written lessons are all locked shows a lock and its first missing prerequisite */
      const lockOf = (st) => {
        const P = Z.prereq, w = st.lessons.filter(l => l.written === true && !done(l));
        if (!P || !w.length || !w.every(l => P.lessonLocked(l.course, l.id))) return null;
        const m = P.missingFor(w[0].course, w[0].id), nd = (m.start && m.start.node) || m.direct[0];
        return nd ? { text: nd.kind === 'lesson' ? nd.name : `${nd.courseName}, level ${nd.n}`, count: m.count, first: w[0] } : { text: 'a prerequisite', count: 1, first: w[0] };
      };
      const stepRow = (st, i) => {
        const s = stepState(st.lessons), { title, sub } = stepTitle(st), lk = lockOf(st);
        const w = st.lessons.filter(l => l.written === true), d = st.lessons.filter(done).length, nw = st.lessons.length - w.length;
        const course = C.course(st.ref.split('/')[0]) || {};
        const facts = [plural(st.lessons.length, 'lesson', 'lessons')];
        if (w.length) facts.push(`${d} done`);
        if (nw) facts.push(`${nw} not yet written`);
        const label = `Step ${i + 1}: ${title}, ${sub}. ${st.priority === 'must' ? 'Must do' : 'Should do'}. ${STATE[s][0]}. ${lk ? `Locked, first missing: ${lk.text}. ` : ''}${facts.join(', ')}.`;
        return `<li class="pp-step is-${s}${lk ? ' is-locked' : ''}" data-track="${esc(course.track || 'prob')}">
          <span class="pp-n tnum" aria-hidden="true">${i + 1}</span>
          <div class="pp-step-b">
            <a class="pp-step-t" href="#course/${esc(st.ref.split('/')[0])}" aria-label="${esc(label)}"><span class="pp-step-name">${esc(title)}</span><span class="pp-step-sub">${esc(sub)}</span></a>
            <div class="pp-chips">
              <span class="pp-pri is-${st.priority}">${st.priority === 'must' ? 'Must' : 'Should'}</span>
              <span class="pp-st is-${s}">${STATE[s][1]}<span>${STATE[s][0]}</span></span>
              ${lk ? `<span class="pp-st is-locked" title="Locked until its prerequisites are met">${Z.icon('lock', 'xs')}<span>Locked</span></span>` : ''}
              ${st.track ? `<span class="pp-role">${esc(roleName(st.track))}</span>` : ''}
              <span class="pp-facts tnum">${esc(facts.join(' · '))}</span>
            </div>
            ${lk ? `<p class="t-caption secondary pp-lock">First missing: ${esc(lk.text)}${lk.count > 1 ? ` (and ${lk.count - 1} more)` : ''}. <a href="#lesson/${esc(lk.first.course)}/${esc(lk.first.id)}">See what is missing</a></p>` : ''}
            <p class="t-body secondary pp-why">${esc(st.why)}</p>
          </div></li>`;
      };

      /* ---------- Picker ---------- */
      const pressed = (b) => ` aria-pressed="${b}"`;
      const picker = () => {
        const modeBar = modes.length > 1 ? `<div class="pp-seg" role="group" aria-label="Prepare for">${modes.map(([k, name]) =>
          `<button type="button" data-mode="${k}"${pressed(sel.mode === k)}>${esc(name)}</button>`).join('')}</div>` : '';
        let more = '';
        if (sel.mode === 'general' && generals.length > 1) more = `<div class="pp-chipsrow" role="group" aria-label="General path">${generals.map(p => `<button type="button" class="pp-pick" data-path="${esc(p.id)}"${pressed(sel.general === p.id)}>${esc(p.name)}</button>`).join('')}</div>`;
        if (sel.mode === 'stage') {
          const stages = STAGES.filter(s => stagePaths.some(p => p.stage === s)), roles = ROLES.filter(r => stagePaths.some(p => p.track === r[0]));
          more = `<div class="pp-two">
            <div class="pp-grp"><span class="t-overline muted">Stage</span><div class="pp-seg is-sm" role="group" aria-label="Stage">${stages.map(s =>
              `<button type="button" data-stage="${s}"${pressed(sel.stage === s)}>${esc(C.prepStageLabel(s))}</button>`).join('')}</div></div>
            <div class="pp-grp"><span class="t-overline muted">Role</span><div class="pp-seg is-sm" role="group" aria-label="Role">${roles.map(([k, name]) =>
              `<button type="button" data-role="${k}"${pressed(sel.role === k)}${stagePaths.some(p => p.stage === sel.stage && p.track === k) ? '' : ' class="is-none"'}>${esc(name)}</button>`).join('')}</div></div>
          </div>`;
        }
        if (sel.mode === 'firm') more = `<div class="pp-chipsrow" role="group" aria-label="Firm">${firms.map(p =>
          `<button type="button" class="pp-pick" data-path="${esc(p.id)}"${pressed(sel.firm === p.id)}>${esc(p.name)}</button>`).join('')}</div>`;
        return modeBar + more;
      };

      /* ---------- The path ---------- */
      const mockRow = (id) => {
        const there = C.mocks().includes(id);
        const name = C.deKebab(id.replace(/^mock-/, ''));
        return there
          ? `<li class="pp-mock" data-mock="${esc(id)}"><span class="pp-mock-ic">${Z.icon('timer', 'sm')}</span><span class="pp-mock-n">${esc(name)}</span><a class="btn secondary pp-mock-go" href="#exam/${esc(id)}">Sit mock</a></li>`
          : `<li class="pp-mock is-nw" data-mock="${esc(id)}"><span class="pp-mock-ic">${Z.icon('timer', 'sm')}</span><span class="pp-mock-n"><code>${esc(id)}</code></span><span class="pp-mock-tag">Not yet written</span></li>`;
      };
      const pathHTML = (p) => {
        if (!p) {
          const what = sel.mode === 'stage' ? `${C.prepStageLabel(sel.stage)} for ${roleName(sel.role).toLowerCase()}` : 'this choice';
          return `<div class="pp-none"><p class="t-body secondary">No path is written for ${esc(what)} yet.</p></div>`;
        }
        const steps = C.prepSteps(p), ds = steps.filter(st => stepState(st.lessons) === 'done').length;
        const month = C.prepMonth(p.asOf);
        const overline = p.kind === 'general' ? 'General' : p.kind === 'stage' ? `${C.prepStageLabel(p.stage)} · ${roleName(p.track)}` : `Firm${p.track ? ' · ' + roleName(p.track) : ''}`;
        const src = p.kind === 'firm' && p.source ? C.prepRefLessons(p.source)[0] : null;
        const pct = steps.length ? Math.round(ds / steps.length * 100) : 0;
        return `<section class="pp-path card" aria-labelledby="pp-path-h">
          <div class="pp-path-head">
            <span class="t-overline muted">${esc(overline)}</span>
            <h2 class="t-h2" id="pp-path-h">${esc(p.name)}</h2>
            ${p.kind === 'firm' ? `<p class="t-label pp-asof">Reported formats, as of ${esc(month || 'a date not given')}</p>` : ''}
            ${p.description ? `<p class="t-body secondary">${esc(p.description)}</p>` : ''}
            ${src ? `<p class="t-caption muted">Source: <a href="#course/${esc(src.course)}">${esc(src.name)}</a>. Formats come from candidate reports and change.</p>` : ''}
          </div>
          ${steps.length ? `<div class="pp-prog"><div class="bar thin track" role="progressbar" aria-label="Steps done" aria-valuemin="0" aria-valuemax="100" aria-valuenow="${pct}"><i style="width:${pct}%"></i></div>
            <span class="t-caption muted tnum">${ds} of ${plural(steps.length, 'step', 'steps')} done</span></div>
          <ol class="pp-steps">${steps.map(stepRow).join('')}</ol>` : '<p class="t-body secondary pp-none">No steps are written for this path yet.</p>'}
          ${(p.mocks || []).length ? `<div class="pp-mocks"><h3 class="t-overline muted" id="pp-mocks-h">Mocks for this path</h3><ul aria-labelledby="pp-mocks-h">${p.mocks.map(mockRow).join('')}</ul></div>` : ''}
        </section>`;
      };

      root.innerHTML = `<div class="pp">
        <header class="pp-head">
          <a class="pp-back" href="#learn">${Z.icon('chevronL', 'sm')}<span>Learn</span></a>
          <h1 class="t-h1">Prepare for</h1>
          <p class="t-body secondary">Pick an assessment or a firm to see which lessons to study first, in order. A step you cannot open yet shows a lock and the first thing missing.</p>
        </header>
        <div class="pp-pick-card" data-picker></div>
        <div data-panel aria-live="polite"></div>
        <p class="t-caption muted pp-foot">Firm formats come from candidate reports and change from cycle to cycle. Check the date under each firm.</p>
      </div>`;
      const pickerEl = root.querySelector('[data-picker]'), panelEl = root.querySelector('[data-panel]');

      const paintPanel = () => {
        panelEl.innerHTML = pathHTML(current());
        /* Mock names come from the exam files, when they are written */
        panelEl.querySelectorAll('.pp-mock:not(.is-nw)').forEach(li => {
          C.exam(li.dataset.mock).then(doc => {
            if (!alive || !doc) return;
            if (doc.name) { const n = li.querySelector('.pp-mock-n'); if (n) n.textContent = doc.name; }
            /* a mock that names requires follows the lock (ENGINE-BACKLOG 487) */
            const P = Z.prereq, go = li.querySelector('.pp-mock-go');
            if (P && go && P.examLocked(doc.id || li.dataset.mock, doc)) { go.innerHTML = `${Z.icon('lock', 'xs')} Locked`; li.classList.add('is-locked'); }
          }).catch(() => { /* keep the id-based name */ });
        });
      };
      const paint = () => { pickerEl.innerHTML = picker(); paintPanel(); };
      const remember = () => {
        const p = current();
        try { if (p) history.replaceState(null, '', '#prepare/' + encodeURIComponent(p.id)); } catch { /* the hash stays as it was */ }
      };
      const focusBack = (sel2) => { const el = pickerEl.querySelector(sel2); if (el) el.focus({ preventScroll: true }); };

      const onClick = (e) => {
        const b = e.target.closest('button'); if (!b || !pickerEl.contains(b)) return;
        if (b.dataset.mode) { sel.mode = b.dataset.mode; paint(); remember(); focusBack(`[data-mode="${sel.mode}"]`); return; }
        if (b.dataset.stage) { sel.stage = b.dataset.stage; if (!stagePaths.some(p => p.stage === sel.stage && p.track === sel.role)) { const f = stagePaths.find(p => p.stage === sel.stage); if (f) sel.role = f.track; } paint(); remember(); focusBack(`[data-stage="${sel.stage}"]`); return; }
        if (b.dataset.role) { sel.role = b.dataset.role; paint(); remember(); focusBack(`[data-role="${sel.role}"]`); return; }
        if (b.dataset.path) { if (sel.mode === 'firm') sel.firm = b.dataset.path; else sel.general = b.dataset.path; paint(); remember(); focusBack(`[data-path="${b.dataset.path}"]`); }
      };
      root.addEventListener('click', onClick);

      let raf = 0;
      onState = () => {
        cancelAnimationFrame(raf);
        raf = requestAnimationFrame(() => { if (!alive || !root.isConnected) return; const y = window.scrollY; paintPanel(); window.scrollTo(0, y); });
      };

      paint();
      return () => { alive = false; onState = null; cancelAnimationFrame(raf); root.removeEventListener('click', onClick); };
    },
  });
})();
